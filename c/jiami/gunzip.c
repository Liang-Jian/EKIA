#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#include "gunzip.h"

const static int LENGTH_EXTRA_BITS[] = {
    0, 0, 0, 0, 0, 0, 0, 0,
    1, 1, 1, 1, 2, 2, 2, 2,
    3, 3, 3, 3, 4, 4, 4, 4,
    5, 5, 5, 5, 0, 99, 99
};

const static int LENGTH_VALUES[] = {
    3, 4, 5, 6, 7, 8, 9, 10,
    11, 13, 15, 17, 19, 23, 27, 31,
    35, 43, 51, 59, 67, 83, 99, 115,
    131, 163, 195, 227, 258, 0, 0
};

const static int DISTANCE_EXTRA_BITS[] = {
    0, 0, 0, 0, 1, 1, 2, 2,
    3, 3, 4, 4, 5, 5, 6, 6,
    7, 7, 8, 8, 9, 9, 10, 10,
    11, 11, 12, 12, 13, 13
};

const static int DISTANCE_VALUES[] = {
    1, 2, 3, 4, 5, 7, 9, 13,
    17, 25, 33, 49, 65, 97, 129, 193,
    257, 385, 513, 769, 1025, 1537, 2049, 3073,
    4097, 6145, 8193, 12289, 16385, 24577
};

const static int DYNAMIC_LENGTH_ORDER[] = {
    16, 17, 18, 0, 8, 7, 9, 6,
    10, 5, 11, 4, 12, 3, 13, 2, 14, 1, 15
};

static void create_huffman_tree(byte *bits, int maxCode, int *tree) {
    int bl_count[MAX_BITS + 1];
    int code = 0, value = 0, left = 0, right = 0, node = 0;
    int next_code[MAX_BITS + 1];
    int len = 0, i = 0, bit = 0;
    int treeInsert = 1;
    
    memset(bl_count, 0, sizeof(bl_count));
    memset(next_code, 0, sizeof(next_code));
    
    for (i = 0; i < maxCode + 1; i++) {
        bl_count[bits[i]]++;
    }
    bl_count[0] = 0;
    
    for (i = 1; i <= MAX_BITS; i++) {
        next_code[i] = code = (code + bl_count[i - 1]) << 1;
    }
    
    for (i = 0; i <= maxCode; i++) {
        len = bits[i];
        if (len != 0) {
            code = next_code[len]++;
            node = 0;
            for (bit = len - 1; bit >= 0; bit--) {
                value = code & (1 << bit);
                if (value == 0) {
                    left = (tree[node] >> 16) & 0xFFFF;
                    if (left == 0) {
                        tree[node] |= (treeInsert << 16);
                        node = treeInsert++;
                    } else {
                        node = left;
                    }
                } else {
                    right = tree[node] & 0xFFFF;
                    if (right == 0) {
                        tree[node] |= treeInsert;
                        node = treeInsert++;
                    } else {
                        node = right;
                    }
                }
            }
            
            tree[node] = 0x80000000 | i;
        }
    }
}

static int read_code(int *tree, struct inflate_context *context) {
    int node = tree[0];
    
    while (node >= 0) {
        if (context->bit == 0) {
            context->byte = (context->compressed[context->index++] & 0xFF);
        }
        
        node = (((context->byte & (1 << context->bit)) == 0) ? tree[node >> 16] : tree[node & 0xFFFF]);
        context->bit = (context->bit + 1) & 7;
    }
    
    return (node & 0xFFFF);
}

static int read_bits(struct inflate_context *context, const int n) {
    int data = (context->bit == 0 ? (context->byte = (context->compressed[context->index++] & 0xFF)) : (context->byte >> context->bit));
    int i;
    
    for (i = (8 - context->bit); i < n; i += 8) {
        context->byte = (context->compressed[context->index++] & 0xFF);
        data |= (context->byte << i);
    }
    
    context->bit = (context->bit + n) & 7;
    return (data & ((1 << n) - 1));
}

static void decode_code_lengths(struct inflate_context *context, int count, byte *bits) {
    int i, code = 0, last = 0, repeat = 0;
    
    for (i = 0, code = 0, last = 0; i < count; ) {
        code = read_code(context->lengths_tree, context);
        if (code >= 16) {
            repeat = 0;
            if (code == 16) {
                repeat = 3 + read_bits(context, 2);
                code = last;
            } else {
                if (code == 17) {
                    repeat = 3 + read_bits(context, 3);
                } else {
                    repeat = 11 + read_bits(context, 7);
                }
                
                code = 0;
            }
            
            while (repeat-- > 0) {
                bits[i++] = (byte) code;
            }
        } else {
            bits[i++] = (byte) code;
        }
        
        last = code;
    }
}

byte* inflate(byte *compressed, int compressed_len, int *uncompressed_len) {
    int flg = 0, uncompressed_index = 0;
    byte *uncompressed;
    int bfinal = 0, btype = 0, len = 0;
    int hlit = 0, hdist = 0, hclen = 0, i = 0;
    byte distance_bits[MAX_CODE_DISTANCES + 1];
    byte length_bits[MAX_CODE_LENGTHS + 1];
    byte literal_bits[MAX_CODE_LITERALS + 1];
    int code = 0, leb = 0, deb = 0;
    int length = 0, distance = 0, offset = 0;
    struct inflate_context context;
    
    memset(distance_bits, 0, sizeof(distance_bits));
    memset(length_bits, 0, sizeof(length_bits));
    memset(literal_bits, 0, sizeof(literal_bits));
    memset(&context, 0, sizeof(struct inflate_context));
    context.compressed = compressed;
    
    if (read_bits(&context, 16) != 0x8B1F || read_bits(&context, 8) != 8) {
        return NULL;
    }
    
    flg = read_bits(&context, 8);
    context.index += 6;
    
    if ((flg & FEXTRA_MASK) != 0) {
        context.index += read_bits(&context, 16);
    }
    
    if ((flg & FNAME_MASK) != 0) {
        while (compressed[context.index++] != 0) {
        }
    }
    
    if ((flg & FCOMMENT_MASK) != 0) {
        while (compressed[context.index++] != 0) {
        }
    }
    
    if ((flg & FHCRC_MASK) != 0) {
        context.index += 2;
    }
    
    context.index = compressed_len - 4;
    *uncompressed_len = read_bits(&context, 16) | (read_bits(&context, 16) << 16);
    uncompressed = (byte *) malloc(*uncompressed_len * sizeof(byte));
    memset(uncompressed, 0, *uncompressed_len * sizeof(byte));
    uncompressed_index = 0;
    bfinal = 0;
    btype = 0;
    
    do {
        bfinal = read_bits(&context, 1);
        btype = read_bits(&context, 2);
        if (bfinal == 0) {
            context.error = ERR_MULTI_SEGMENTS;
            return NULL;
        }
        
        if (btype == BTYPE_NONE) { // 无压缩
            context.bit = 0;
            len = read_bits(&context, 16);
            read_bits(&context, 16);
            memcpy(uncompressed + uncompressed_index, compressed + context.index, len);
            context.index += len;
            uncompressed_index += len;
        } else if (btype == BTYPE_DYNAMIC) { // 动态Huffman
            hlit = read_bits(&context, 5) + 257;
            if (hlit - 1 > MAX_CODE_LITERALS) {
                context.error = ERR_LITERALS_NUM;
                return NULL;
            }
            
            hdist = read_bits(&context, 5) + 1;
            if (hdist - 1 > MAX_CODE_DISTANCES) {
                context.error = ERR_DISTANCES_NUM;
                return NULL;
            }
            
            hclen = read_bits(&context, 4) + 4;
            for (i = 0; i < hclen; i++) {
                length_bits[DYNAMIC_LENGTH_ORDER[i]] = (byte) read_bits(&context, 3);
            }
            
            context.lengths_num = MAX_CODE_LENGTHS;
            create_huffman_tree(length_bits, MAX_CODE_LENGTHS, context.lengths_tree);
            
            context.literals_num = hlit - 1;
            decode_code_lengths(&context, hlit, literal_bits);
            create_huffman_tree(literal_bits, hlit - 1, context.literals_tree);
            
            context.distances_num = hdist - 1;
            decode_code_lengths(&context, hdist, distance_bits);
            create_huffman_tree(distance_bits, hdist - 1, context.distances_tree);
        } else { // 静态Huffman
            for (int i = 0; i < 144; i++) {
                literal_bits[i] = 8;
            }
            
            for (int i = 144; i < 256; i++) {
                literal_bits[i] = 9;
            }
            
            for (int i = 256; i < 280; i++) {
                literal_bits[i] = 7;
            }
            
            for (int i = 280; i < 288; i++) {
                literal_bits[i] = 8;
            }
            
            create_huffman_tree(literal_bits, MAX_CODE_LITERALS, context.literals_tree);
            
            for (int i = 0; i < MAX_CODE_DISTANCES + 1; i++) {
                distance_bits[i] = 5;
            }
            
            create_huffman_tree(distance_bits, MAX_CODE_DISTANCES, context.distances_tree);
        }
        
        code = leb = deb = 0;
        while ((code = read_code(context.literals_tree, &context)) != EOB_CODE) {
            if (code > EOB_CODE) {
                code -= 257;
                length = LENGTH_VALUES[code];
                if ((leb = LENGTH_EXTRA_BITS[code]) > 0) {
                    length += read_bits(&context, leb);
                }
                
                code = read_code(context.distances_tree, &context);
                distance = DISTANCE_VALUES[code];
                if ((deb = DISTANCE_EXTRA_BITS[code]) > 0) {
                    distance += read_bits(&context, deb);
                }
                
                offset = uncompressed_index - distance;
                while (distance < length) {
                    memcpy(uncompressed + uncompressed_index, uncompressed + offset, distance);
                    uncompressed_index += distance;
                    length -= distance;
                    distance <<= 1;
                }
                
                memcpy(uncompressed + uncompressed_index, uncompressed + offset, length);
                uncompressed_index += length;
            } else {
                uncompressed[uncompressed_index++] = (byte) code;
            }
        }
    } while (bfinal == 0);
    
    return uncompressed;
}
