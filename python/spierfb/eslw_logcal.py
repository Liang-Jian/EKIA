# coding=utf-8
# author: huzhiyu
import re
import numpy as np
import datetime

eslfile = 'esl28.txt'
esls = [] #价签
store = 'god.1'

def getEslList():
    try:
        file_path = eslfile
        with open(file_path, 'r') as f:
            for lineb in f:
                if lineb:
                    esls.append(lineb.replace('\n',''))
    except(Exception,) as f:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),',esl load error:',f)
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),',esl loaded,length=',len(esls))

def getDataFromLog(eslw):
    receive = []
    signin = []
    ack_status = []
    ack_result = []
    esl_update_finished = []
    heatp_data = []
    ap_result = []
    session_created = []
    uplink_single_package =[]
    multicast_receive = []
    quick_flash = []
    multicast_signin = []
    multicast_finish = []
    send_quick_cmd = []
    send_global_cmd = []
    send_set_cmd = []
    set_cmd_ack = []
    with open(eslw, 'r',encoding='utf-8') as f:
        for lineb in f:
            if r := re.match('(.{23}).*action=receive,.*user_code=(.*?),eslid=(.*?),payload_type=UPDATE,payload_retry_time=(.*?)',lineb):
                if r.group(2) == store:
                    receive.append([r.group(1),r.group(2),r.group(3),r.group(4)])
            if r := re.match('(.{23}).*action=signin,.*user_code=(.*?),eslid=(.*?),payload_type=UPDATE,.*ap_mac=(.*?),unit=(.*?)',lineb):
                if r.group(2) == store:
                    signin.append([r.group(1),r.group(2),r.group(3),r.group(4),r.group(5)])
            if r := re.match('(.{23}).*action=heatp_data,.*user_code=(.*?),.*ap_mac=(.*?),task_id=(.*?),unitUUID=\[(.*?)\],setwor=(.*?),.*esl_amount=(.*?),.*latched_channels=\[(.*?)\],.*',lineb):
                heatp_data.append([r.group(1),r.group(2),r.group(3),r.group(4),r.group(5),r.group(6),r.group(7),r.group(8)])
            if r := re.match('(.{23}).*action=ack_result,user_code=(.*?),.*ap_mac=(.*?),task_id=(.*?),total_amount=(.*?),prior_payload_type=UPDATE,.*detail=\{(.*?)\}',lineb):
                ap_result.append([r.group(1),r.group(2),r.group(3),r.group(4),r.group(5),r.group(6)])
            if r := re.match('(.{23}).*ExecutorGroup-(.*?)\].*action=session_created,.*user_code=(.*?),.*eslid=(.*?),payload_type=UPDATE,.*,byte_size=(\d+),.*,time=(\d+),.*',lineb):
                session_created.append([r.group(1),r.group(2),r.group(3),r.group(4),int(r.group(5)),int(r.group(6))])
            if r := re.match('(.{23}).*action=ack_status,.*user_code=(.*?),.*eslid=(.*?),.*ap_mac=(.*?),.*payload_type=UPDATE,.*payload_retry_time=(.*?),.*success=(.*?),.*success_num=(.*?),.*fail_num=(.*?),.*',lineb):
                ack_status.append([r.group(1),r.group(2),r.group(3),r.group(4),r.group(5),r.group(6),r.group(7),r.group(8)])
            if r := re.match('(.{23}).*action=uplink_single_package,.*,eslId=(.*?),type=6,.*',lineb):
                uplink_single_package.append([r.group(1),r.group(2)])
            if r := re.match('(.{23}).*action=ack_result,.*user_code=(.*?),eslid=(.*?),type=UPDATE,payload_retry_time=(.*?),total_retry_time=(.*?),result=(.*?),ack_value=(.*?),.*work_time=(.*)',lineb):
                ack_result.append([r.group(1),r.group(2),r.group(3),r.group(4),r.group(5),r.group(6),r.group(7),r.group(8)])
            if r := re.match('(.{23}).*action=esl_update_finished,.*user_code=(.*?),eslid=(.*?),status=(.*?),total_retry_time=(.*?),millisecond=(.*)',lineb):
                if r.group(2) == store:
                    esl_update_finished.append([r.group(1),r.group(2),r.group(3),r.group(4),r.group(5),r.group(6)])
            if r := re.match('(.{23}).*action=multicast_receive,.*user_code=(.*?),esl_id=(.*?),.*',lineb):
                multicast_receive.append([r.group(1),r.group(2),r.group(3)])
            if r := re.match('(.{23}).*action=multicast_signin,.*user_code=(.*?),esl_id=(.*?),ap_mac=(.*?),uuid=(.*?),.*',lineb):
                multicast_signin.append([r.group(1),r.group(2),r.group(3),r.group(4),r.group(5)])
            # if r := re.match('(.{23}).*action=quick_flash,.*user_code=(.*?),ap_mac=(.*?),eslid=(.*?),.*operate_type=(.*?),.*',lineb):
            #     quick_flash.append([r.group(1),r.group(2),r.group(3),r.group(4),r.group(5)])

            if r := re.match('(.{23}).*action=multicast_finish,user_code=(.*?),esl_id=(.*?),ap_mac=(.*?),.*ack=(.*?),retry_time=(.*?),work_time=(.*)',lineb):
                multicast_finish.append([r.group(1),r.group(2),r.group(3),r.group(4),r.group(5),r.group(6),r.group(7)])
            if r := re.match('(.{23}).*action=send_quick_cmd,user_code=(.*?),ap_mac=(.*?),task_id=(.*?),uuid=(.*?),.*,channel=(.*?),.*esl_amount=(.*?),.*',lineb):
                send_quick_cmd.append([r.group(1),r.group(2),r.group(3),r.group(4),r.group(5),r.group(6),r.group(7)])
            if r := re.match('(.{23}).*action=send_global_cmd,user_code=(.*?),ap_mac=(.*?),task_id=(.*?),setUUID=(.*?),channel=(.*?),.*cmd=(.*?),.*esl_amount=(.*?),.*',lineb):
                send_global_cmd.append([r.group(1),r.group(2),r.group(3),r.group(4),r.group(5),r.group(6),r.group(7),r.group(8)])
            if r := re.match('(.{23}).*action=send_set_cmd,user_code=(.*?),.*,ap_mac=(.*?),task_id=(.*?),duration=(.*)',lineb):
                send_set_cmd.append([r.group(1),r.group(2),r.group(3),r.group(4),r.group(5)])
            if r := re.match('(.{23}).*action=set_cmd_ack,user_code=(.*?),ap_mac=(.*?),task_id=(.*?),.*,esl_amount=(.*?),detail=\{(.*?)\}',lineb):
                set_cmd_ack.append([r.group(1),r.group(2),r.group(3),r.group(4),r.group(5),r.group(6)])
    # with open(uplink, 'r') as f:
    #     for lineb in f:
    #         if r := re.match('(.{23}).*action=uplink_single_package,.*,eslId=(.*?),type=6,.*',lineb):
    #                 uplink_single_package.append([r.group(1),r.group(2)])
    return receive,signin,heatp_data,ap_result,session_created,ack_status,uplink_single_package,ack_result,esl_update_finished,multicast_receive,quick_flash,multicast_signin,multicast_finish,send_quick_cmd,send_global_cmd,send_set_cmd,set_cmd_ack

def calUpdate(receive_l,signin_l,heatp_data_l,ap_result_l,session_created_l,ack_status_l,uplink_single_package_l,ack_result_l,esl_update_finished_l):
    wor_data = []
    tasks = list(set(np.array(ap_result_l)[:,3]))
    for tmp in heatp_data_l:
        if tmp[3] in tasks:
            wor_data.append(tmp[4].split(':')[-1]+':'+str(tmp[5]))
    unique,count = np.unique(np.array(wor_data),return_counts=True)
    wor_map = dict(zip(unique,count))

    ew_start = receive_l[0][0]
    ew_end = esl_update_finished_l[len(esl_update_finished_l)-1][0]
    
    # succ_cost_time = 0
    # for i in range(len(esl_update_finished_l)-1,0,-1):
    #     if esl_update_finished_l[i][3] == 'online':
    #         succ_cost_time = datetime.datetime.strptime(esl_update_finished_l[i][0], '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(ew_start, '%Y-%m-%d %H:%M:%S.%f')
    #         succ_cost_time = str(int(succ_cost_time.seconds/60)) + '分' + str(succ_cost_time.seconds%60) + '秒'
    #         break
    
    total_cost_time = datetime.datetime.strptime(ew_end, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(ew_start, '%Y-%m-%d %H:%M:%S.%f')
    total_cost_time = str(int(total_cost_time.seconds/60)) + '分' + str(total_cost_time.seconds%60) + '秒'

    esl_cnt = len(set(np.array(receive_l)[:,2]))
    receive_cnt = len(receive_l)
    finish_cnt = len(esl_update_finished_l)
    avg_byte_128 = round(sum(np.array(session_created_l)[:,4].astype(int))/len(session_created_l)/128,2)
    heatp_cnt = len(ap_result_l)
    ap_cnt = len(set(np.array(ap_result_l)[:,2])) if len(ap_result_l)>0 else 0

    unique,count = np.unique(np.array(ack_result_l)[:,6],return_counts=True)
    ack_map = dict(zip(unique,count))

    unique,count = np.unique(np.array(ack_result_l)[:,3],return_counts=True)
    payload_retry_map = dict(zip(unique,count))
    payload_retry_map.pop('0',None)

    unique,count = np.unique(np.array(ack_result_l)[:,4],return_counts=True)
    total_retry_map = dict(zip(unique,count))
    total_retry_map.pop('0',None)

    fail_esls = []
    update_result_cnt = 0
    for tmp in esl_update_finished_l:
        if tmp[3] != 'online':
            fail_esls.append(tmp[2])
        if tmp[3] == 'online':
            update_result_cnt = update_result_cnt + 1

    fail_esls = list(set(fail_esls))
    fail_esls_cnt = 0
    fail_esls_cnt = len(fail_esls)
    print(fail_esls)
    if fail_esls_cnt < 1:
        fail_esls_cnt = str(fail_esls)

    fail_lose_esls = []
    lose_esls = []
    for tmp in signin_l:
        if tmp[2] in fail_esls and tmp[4][:-5]=='false':
            fail_lose_esls.append(tmp[2])
        if tmp[4][:-5]=='false':
            lose_esls.append(tmp[2])
    print('lose_esls_len=',len(list(set(lose_esls))))
    fail_lose_esls = list(set(fail_lose_esls))
    fail_lose_cnt = 0
    fail_lose_cnt = len(fail_lose_esls)

    print(list(set(fail_lose_esls)))
    if fail_lose_cnt < 1:
        fail_lose_cnt = str(fail_lose_esls)

    comm_succ_rate = 0
    sum_succ_pack = sum(np.array(ack_status_l)[:,6].astype(int))
    sum_fail_pack = sum(np.array(ack_status_l)[:,7].astype(int))
    total_pack = sum_succ_pack + sum_fail_pack
    comm_succ_rate = str(round(sum_succ_pack*100/total_pack,2))+'%'

    err_code = []
    once_succ_cnt = 0
    for tmp in ack_result_l:
        if tmp[6]!='64' and tmp[6]!='0':
            err_code.append([tmp[2],tmp[6]])
        if tmp[6]=='64' and tmp[4]=='0':
            once_succ_cnt = once_succ_cnt + 1
        # if tmp[6]=='64':
        #     update_result_cnt = update_result_cnt + 1
    update_succ_rate = str(round(update_result_cnt*100/finish_cnt,2))+'%'
    once_succ_rate = str(round(once_succ_cnt*100/finish_cnt,2))+'%'

    worktime_array = np.sort(np.array(ack_result_l)[:,7].astype(int))
    worktime_20 = str(round(worktime_array[int(len(worktime_array)*0.2)]/1000/60,2))+'分钟' if round(worktime_array[int(len(worktime_array)*0.2)]/1000) > 60 else str(round(worktime_array[int(len(worktime_array)*0.2)]/1000))+'秒'
    worktime_40 = str(round(worktime_array[int(len(worktime_array)*0.4)]/1000/60,2))+'分钟' if round(worktime_array[int(len(worktime_array)*0.4)]/1000) > 60 else str(round(worktime_array[int(len(worktime_array)*0.4)]/1000))+'秒'
    worktime_60 = str(round(worktime_array[int(len(worktime_array)*0.6)]/1000/60,2))+'分钟' if round(worktime_array[int(len(worktime_array)*0.6)]/1000) > 60 else str(round(worktime_array[int(len(worktime_array)*0.6)]/1000))+'秒'
    worktime_80 = str(round(worktime_array[int(len(worktime_array)*0.8)]/1000/60,2))+'分钟' if round(worktime_array[int(len(worktime_array)*0.8)]/1000) > 60 else str(round(worktime_array[int(len(worktime_array)*0.8)]/1000))+'秒'
    worktime_90 = str(round(worktime_array[int(len(worktime_array)*0.9)]/1000/60,2))+'分钟' if round(worktime_array[int(len(worktime_array)*0.9)]/1000) > 60 else str(round(worktime_array[int(len(worktime_array)*0.9)]/1000))+'秒'
    worktime_99 = str(round(worktime_array[int(len(worktime_array)*0.99)]/1000/60,2))+'分钟' if round(worktime_array[int(len(worktime_array)*0.99)]/1000) > 60 else str(round(worktime_array[int(len(worktime_array)*0.99)]/1000))+'秒'
    worktime_100 = str(round(worktime_array[len(worktime_array)-1]/1000/60,2))+'分钟' if round(worktime_array[len(worktime_array)-1]/1000) > 60 else str(round(worktime_array[len(worktime_array)-1]/1000))+'秒'

    thread_cnt = len(set(np.array(session_created_l)[:,1]))

    pack_speed = str(round(sum(np.array(session_created_l)[:,4].astype(int))/sum(np.array(session_created_l)[:,5].astype(int)),2))+'KB/s'
    #漫游
    roam= []
    if(len(uplink_single_package_l)>0):
        roam = set(np.array(uplink_single_package_l)[:,1])
    roam_fail_cnt,roam_succ_cnt = '',''
    if len(roam) > 0:
        roam_fail_cnt = 0
        for tmp in roam:
            if tmp in fail_esls:
                roam_fail_cnt = roam_fail_cnt + 1
        roam_succ_cnt = len(roam) - roam_fail_cnt
    if len(roam)>1:
        roam = len(roam)
    return [wor_map,esl_cnt,ew_start,ew_end,total_cost_time,receive_cnt,finish_cnt,avg_byte_128,heatp_cnt,ap_cnt,ack_map,payload_retry_map,total_retry_map,
            comm_succ_rate,fail_esls_cnt,fail_lose_cnt,roam,update_succ_rate,worktime_20,worktime_40,worktime_60,worktime_80,worktime_90,worktime_99,worktime_100,thread_cnt,pack_speed,once_succ_rate,roam_succ_cnt,roam_fail_cnt]

def genAPTableHtml(business,sub,arr):
    table = '<h3>'+business+'--'+sub
    table += '<table class="bordered"><thead><tr>'
    for i in ('开始','结束','耗时(秒)','基站MAC', '任务', 'uuid', '信道', '数量', '听帧','结果'):
        table += '<th scope="col" nowrap="nowrap">' + i + '</th>'
    table += '</tr>'

    for tmp in arr:
        table += '<tr>'
        for tmp1 in tmp:
            table += '<td scope="col">' + str(tmp1) + '</td>'
        table += '</tr>'
    table += '</table><br>'
    return table

def genGlobalAPTableHtml(business,sub,arr):
    table = '<h3>'+business+'--'+sub
    table += '<table class="bordered"><thead><tr>'
    for i in ('开始','结束','耗时(秒)','基站MAC', '任务', 'uuid', '信道', '命令', '数量', '听帧','结果'):
        table += '<th scope="col" nowrap="nowrap">' + i + '</th>'
    table += '</tr>'

    for tmp in arr:
        table += '<tr>'
        for tmp1 in tmp:
            table += '<td scope="col">' + str(tmp1) + '</td>'
        table += '</tr>'
    table += '</table><br>'
    return table

def genTableHtml(type,business,sub,arr):
    table = '<h3>'+business
    table += '<table class="bordered"><thead><tr>'
    if type==0:
        del arr[4]
        for i in ('业务','任务听帧数','价签数量', '开始时间', '结束时间', 'receive', 'finish','平均byte数/128','下发次数','基站数量','ack','payload_retry','total_retry',
                '通信成功率','失败价签','失败且失步价签','申请漫游','更新成功率','worktime_20%','worktime_40%','worktime_60%','worktime_80%','worktime_90%','worktime_99%','worktime_100%','线程数','打包速率','一次成功占比','漫游成功数量','漫游失败数量'):
            if i in ('失败价签','ack','任务听帧数','payload_retry','total_retry'):
                table += '<th scope="col" nowrap="nowrap" width="200">' + i + '</th>'
            elif i in ('业务'):
                table += '<th scope="col" nowrap="nowrap" width="100">' + i + '</th>'
            else:
                table += '<th scope="col" nowrap="nowrap">' + i + '</th>'
    elif type==1:
        del arr[10]
        del arr[9]
        del arr[5]
        del arr[4]
        del arr[0]
        for i in ('业务','价签数量', '开始时间', '结束时间', 'receive', 'finish','平均byte数/128','ack','payload_retry','total_retry',
                '通信成功率','失败价签','失败且失步价签','申请漫游','错误码','更新成功率','worktime_20%','worktime_40%','worktime_60%','worktime_80%','worktime_90%','worktime_99%','worktime_100%','线程数','打包速率','一次成功占比','漫游成功数量','漫游失败数量'):
            if i in ('失败价签','ack','任务听帧数','失败且失步价签','payload_retry','total_retry'):
                table += '<th scope="col" nowrap="nowrap" width="200">' + i + '</th>'
            elif i in ('业务'):
                table += '<th scope="col" nowrap="nowrap" width="100">' + i + '</th>'
            else:
                table += '<th scope="col" nowrap="nowrap">' + i + '</th>'
    elif type==2:
        del arr[2]
        for i in ('业务', '开始时间', '结束时间','价签数量', 'receive','finish','ack','失败价签','失败且失步价签','retry','成功率','一次成功占比','worktime_20%','worktime_40%','worktime_60%','worktime_80%','worktime_90%','worktime_99%','worktime_100%'):
            if i in ('失败价签','ack','任务听帧数','失败且失步价签','retry','payload_retry','total_retry'):
                table += '<th scope="col" nowrap="nowrap" width="200">' + i + '</th>'
            elif i in ('业务'):
                table += '<th scope="col" nowrap="nowrap" width="100">' + i + '</th>'
            else:
                table += '<th scope="col" nowrap="nowrap">' + i + '</th>'
    elif type==3:
        for i in ('业务', '开始时间', '结束时间', '任务听帧数','下发次数','基站数量'):
            table += '<th scope="col" nowrap="nowrap">' + i + '</th>'
    elif type==4:
        for i in ('业务', '开始时间', '结束时间', '下发次数','基站数量'):
            table += '<th scope="col" nowrap="nowrap">' + i + '</th>'
    table += '</tr><tr>'
    table += '<td scope="col">' + sub + '</td>'
    for tmp in arr:
        table += '<td scope="col">' + changeColor(str(tmp)) + '</td>'
    table += '</tr></table><br>'
    return table

def changeColor(str):
    if len(str)>0:
        if str[-1]=='%':
            if float(str[0:-1])>=98:
                return '<font color="green">'+str+'</font>'
            elif float(str[0:-1])>=90:
                return '<font color="#FFA500">'+str+'</font>'
            elif float(str[0:-1])<90:
                return '<font color="red">'+str+'</font>'
    return str

def genHtmlFile(logFile,esls,day_start,day_end):
    filename = 'logcal_wow_'+ datetime.datetime.now().strftime('%Y-%m-%d') + '.html'
    head=get_html_head()

    receive,signin,heatp_data,ap_result,session_created,ack_status,uplink_single_package,ack_result,esl_update_finished,multicast_receive,quick_flash,multicast_signin,multicast_finish,send_quick_cmd,send_global_cmd,send_set_cmd,set_cmd_ack = getDataFromLog(logFile)
    print(len(receive))
    print(len(signin))
    print(len(heatp_data))
    print(len(ap_result))
    print(len(session_created))
    print(len(ack_status))
    print(len(ack_result))
    print(len(uplink_single_package))
    print(len(esl_update_finished))
    print(len(multicast_receive))
    print(len(multicast_signin))
    print(len(quick_flash))
    print(len(multicast_finish))
    print(len(send_quick_cmd))
    print(len(send_global_cmd))
    print(len(send_set_cmd))
    print(len(set_cmd_ack))

    receive = filterEslLogData(receive,2,esls,day_start,day_end)
    signin = filterEslLogData(signin,2,esls,day_start,day_end)
    heatp_data = filterApLogData(heatp_data,day_start,day_end)
    ap_result = filterApLogData(ap_result,day_start,day_end)
    session_created = filterEslLogData(session_created,3,esls,day_start,day_end)
    ack_status = filterEslLogData(ack_status,2,esls,day_start,day_end)
    uplink_single_package = filterEslLogData(uplink_single_package,1,esls,day_start,day_end)
    ack_result = filterEslLogData(ack_result,2,esls,day_start,day_end)
    esl_update_finished = filterEslLogData(esl_update_finished,2,esls,day_start,day_end)
    set_cmd_ack = filterApLogData(set_cmd_ack,day_start,day_end)
    send_quick_cmd = filterApLogData(send_quick_cmd,day_start,day_end)
    send_global_cmd = filterApLogData(send_global_cmd,day_start,day_end)
    send_set_cmd = filterApLogData(send_set_cmd,day_start,day_end)
    multicast_receive = filterEslLogData(multicast_receive,2,esls,day_start,day_end)
    multicast_signin = filterEslLogData(multicast_signin,2,esls,day_start,day_end)
    multicast_finish = filterEslLogData(multicast_finish,2,esls,day_start,day_end)

    print('after filter')
    print(len(receive))
    print(len(signin))
    print(len(heatp_data))
    print(len(ap_result))
    print(len(session_created))
    print(len(ack_status))
    print(len(ack_result))
    print(len(uplink_single_package))
    print(len(esl_update_finished))
    print(len(multicast_receive))
    print(len(multicast_signin))
    print(len(quick_flash))
    print(len(multicast_finish))
    print(len(send_quick_cmd))
    print(len(send_global_cmd))
    print(len(send_set_cmd))
    print(len(set_cmd_ack))

    table = ''
    tableap = ''
    if(len(receive)>0):
        tableap += genUpdateApTable('基站','更新',heatp_data,ap_result)
        table += genUpdateTaskTable(0,'更新','更新',receive,signin,heatp_data,ap_result,session_created,ack_status,uplink_single_package,ack_result,esl_update_finished)
    
    if(len(multicast_receive)>0):
        table += genFlashTaskTable(2,'快闪快切','快闪快切',multicast_receive,quick_flash,multicast_signin,multicast_finish)
        tableap += genFlashApTable('基站','快闪快切',send_quick_cmd,send_set_cmd,set_cmd_ack)
    tableap += genGlobalApTable('基站','全局命令',send_global_cmd,send_set_cmd,set_cmd_ack)
    html = '<html>' + head + '<body>' + table + tableap +'</body>' + '</html>'

    f=open(filename,'w',encoding='utf-8')
    print(html,file=f)

def genFlashTaskTable(ktype,desc,subd,multicast_receive,quick_flash,multicast_signin,multicast_finish):
    result = calFlash(multicast_receive,multicast_signin,multicast_finish)

    table = genTableHtml(ktype,desc,subd,result)
    return table

def genUpdateTaskTable(ktype,desc,subd,receive,signin,heatp_data,ap_result,session_created,ack_status,uplink_single_package,ack_result,esl_update_finished):
    result = calUpdate(receive,signin,heatp_data,ap_result,session_created,ack_status,uplink_single_package,ack_result,esl_update_finished)

    table = genTableHtml(ktype,desc,subd,result)
    return table

def genUpdateApTable(desc,sub,heatp_data,ap_result):
    result = calUpdateApData(heatp_data,ap_result)
    table = genAPTableHtml(desc,sub,result)
    return table

def genFlashApTable(desc,sub,send_quick_cmd,send_set_cmd,set_cmd_ack):
    result = calFlashApData(send_quick_cmd,send_set_cmd,set_cmd_ack)
    table = genAPTableHtml(desc,sub,result)
    return table

def genGlobalApTable(desc,sub,send_global_cmd,send_set_cmd,set_cmd_ack):
    result = calGlobalApData(send_global_cmd,send_set_cmd,set_cmd_ack)
    table = genGlobalAPTableHtml(desc,sub,result)
    return table

def filterEslLogData(logdata,index,esls,start,end):
    result = []
    for tmp in logdata:
        if tmp[0] < start:
            continue
        elif tmp[0] > end:
            break
        elif tmp[index] in esls or len(esls)==0:
            result.append(tmp)
    return result

def filterApLogData(logdata,start,end):
    result = []
    for tmp in logdata:
        if tmp[0] < start:
            continue
        elif tmp[0] > end:
            break
        else:
            result.append(tmp)
    return result

def calUpdateApData(heatp_data_l,ap_result_l):
    # '开始','结束','耗时(秒)','基站MAC', '任务', 'uuid', '信道', '数量', '听帧','结果'
    taskdict = {}
    for tmp in ap_result_l:
        tmpvalue = []
        tmpvalue.append(tmp[0]) #end
        tmpvalue.append(tmp[2]) #apmac
        tmpvalue.append(tmp[3]) #task
        tmpvalue.append(tmp[4]) #数量
        tmpvalue.append('{'+tmp[5]+'}') #detail
        taskdict[tmp[2]+'|'+tmp[3]] = tmpvalue
    for tmp in heatp_data_l:
        if tmp[2]+'|'+tmp[3] in taskdict.keys():
            tmpvalue = taskdict[tmp[2]+'|'+tmp[3]]
            tmpvalue.insert(0,tmp[0])
            tmpvalue.insert(2,(datetime.datetime.strptime(tmpvalue[1],'%Y-%m-%d %H:%M:%S.%f')-datetime.datetime.strptime(tmpvalue[0],'%Y-%m-%d %H:%M:%S.%f')).total_seconds())
            tmpvalue.insert(5,tmp[4])
            tmpvalue.insert(6,tmp[7])
            tmpvalue.insert(8,tmp[5])
            taskdict[tmp[2]+'|'+tmp[3]] = tmpvalue
    return list(taskdict.values())

def calFlashApData(quick_data_l,set_data_l,ack_data_l):
    taskdict = {}
    for tmp in quick_data_l:
        tmpvalue = []
        tmpvalue.append(tmp[0]) #start
        tmpvalue.append(tmp[2]) #apmac
        tmpvalue.append(tmp[3]) #task
        tmpvalue.append(tmp[4]) #uuid
        tmpvalue.append(tmp[5]) #channel
        tmpvalue.append(tmp[6]) #count
        taskdict[tmp[2]+'|'+tmp[3]] = tmpvalue
    
    for tmp in set_data_l:
        if tmp[2]+'|'+tmp[3] in taskdict.keys():
            tmpvalue = taskdict[tmp[2]+'|'+tmp[3]]
            tmpvalue.append(tmp[4])
            taskdict[tmp[2]+'|'+tmp[3]] = tmpvalue
    
    for tmp in ack_data_l:
        if tmp[2]+'|'+tmp[3] in taskdict.keys():
            tmpvalue = taskdict[tmp[2]+'|'+tmp[3]]
            tmpvalue.insert(1,tmp[0])
            tmpvalue.insert(2,(datetime.datetime.strptime(tmp[0],'%Y-%m-%d %H:%M:%S.%f')-datetime.datetime.strptime(tmpvalue[0],'%Y-%m-%d %H:%M:%S.%f')).total_seconds())
            tmpvalue.append('{'+tmp[5]+'}')
            taskdict[tmp[2]+'|'+tmp[3]] = tmpvalue
    return list(taskdict.values())

def calGlobalApData(global_data_l,set_data_l,ack_data_l):
    taskdict = {}
    for tmp in global_data_l:
        tmpvalue = []
        tmpvalue.append(tmp[0]) #start
        tmpvalue.append(tmp[2]) #apmac
        tmpvalue.append(tmp[3]) #task
        tmpvalue.append(tmp[4]) #uuid
        tmpvalue.append(tmp[5]) #channel
        tmpvalue.append(tmp[6]) #cmd
        tmpvalue.append(tmp[7]) #detail
        if tmp[6] != 'EslSyncTask':
            taskdict[tmp[2]+'|'+tmp[3]] = tmpvalue
    
    for tmp in set_data_l:
        if tmp[2]+'|'+tmp[3] in taskdict.keys():
            tmpvalue = taskdict[tmp[2]+'|'+tmp[3]]
            tmpvalue.append(tmp[4])
            taskdict[tmp[2]+'|'+tmp[3]] = tmpvalue

    for tmp in ack_data_l:
        if tmp[2]+'|'+tmp[3] in taskdict.keys():
            tmpvalue = taskdict[tmp[2]+'|'+tmp[3]]
            tmpvalue.insert(1,tmp[0])
            tmpvalue.insert(2,(datetime.datetime.strptime(tmp[0],'%Y-%m-%d %H:%M:%S.%f')-datetime.datetime.strptime(tmpvalue[0],'%Y-%m-%d %H:%M:%S.%f')).total_seconds())
            tmpvalue.append('{'+tmp[5]+'}')
            taskdict[tmp[2]+'|'+tmp[3]] = tmpvalue
    return list(taskdict.values())

def calFlash(multi_receive_l,multi_signin_l,multi_finish_l):
    start_time = multi_receive_l[0][0]
    end_time = multi_finish_l[-1][0]
    cost_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
    cost_time = str(int(cost_time.seconds/60)) + '分' + str(cost_time.seconds%60) + '秒'
    esl_cnt = len(set(np.array(multi_receive_l)[:,2]))
    receive_cnt = len(multi_receive_l)
    finish_cnt = len(multi_finish_l)

    unique,count = np.unique(np.array(multi_finish_l)[:,4],return_counts=True)
    ack_map = dict(zip(unique,count))

    succ_cnt,one_succ_cnt = 0,0
    fail_esls = []
    for tmp in multi_finish_l:
        if tmp[4] == '64':
            succ_cnt = succ_cnt + 1
            if tmp[5] == '0':
                one_succ_cnt = one_succ_cnt + 1
        else:
            fail_esls.append(tmp[2])
    succ_rate = str(round(succ_cnt*100/len(multi_finish_l),2))+'%'
    one_succ_rate = str(round(one_succ_cnt*100/len(multi_finish_l),2))+'%'
    fail_esls = list(set(fail_esls))
    fail_lose_esls = []
    lose_esls = []
    for tmp in multi_signin_l:
        if tmp[2] in fail_esls and '-false-' in tmp[4]:
            fail_lose_esls.append(tmp[2])
        if '-false-' in tmp[4]:
            lose_esls.append(tmp[2])
    print('lose_esls_len=',len(list(set(lose_esls))))
    fail_lose_esls = list(set(fail_lose_esls))
    print(list(set(fail_esls)))
    if len(list(set(fail_esls)))>0:
        fail_esls = len(list(set(fail_esls)))
        fail_lose_esls = len(list(set(fail_lose_esls)))
    
    unique,count = np.unique(np.array(multi_finish_l)[:,5],return_counts=True)
    total_retry_map = dict(zip(unique,count))
    total_retry_map.pop('0',None)

    worktime_array = np.sort(np.array(multi_finish_l)[:,6].astype(int))
    worktime_20 = str(round(worktime_array[int(len(worktime_array)*0.2)]/1000,2))+'秒'
    worktime_40 = str(round(worktime_array[int(len(worktime_array)*0.4)]/1000,2))+'秒'
    worktime_60 = str(round(worktime_array[int(len(worktime_array)*0.6)]/1000,2))+'秒'
    worktime_80 = str(round(worktime_array[int(len(worktime_array)*0.8)]/1000,2))+'秒'
    worktime_90 = str(round(worktime_array[int(len(worktime_array)*0.9)]/1000,2))+'秒'
    worktime_99 = str(round(worktime_array[int(len(worktime_array)*0.99)]/1000,2))+'秒'
    worktime_100 = str(round(worktime_array[len(worktime_array)-1]/1000,2))+'秒'

    return [start_time,end_time,cost_time,esl_cnt,receive_cnt,finish_cnt,ack_map,fail_esls,fail_lose_esls,total_retry_map,succ_rate,one_succ_rate,worktime_20,worktime_40,worktime_60,worktime_80,worktime_90,worktime_99,worktime_100]

def get_html_head():
    head = """<head><meta charset="utf-8">
        <style type="text/css" MEDIA=screen>
        h2 {
            color: black;
        }

        table {
            *border-collapse: collapse; /* IE7 and lower */
            border-spacing: 0;
            width: 95%;
        }

        .bordered {
            border: solid #ccc 1px;
            -moz-border-radius: 1px;
            -webkit-border-radius: 1px;
            border-radius: 1px;
            -webkit-box-shadow: 0 1px 1px #ccc;
            -moz-box-shadow: 0 1px 1px #ccc;
            box-shadow: 0 1px 1px #ccc;
            margin-top:5px;
        }

        .bordered tr:hover {
            background: #fbf8e9;
            -o-transition: all 0.1s ease-in-out;
            -webkit-transition: all 0.1s ease-in-out;
            -moz-transition: all 0.1s ease-in-out;
            -ms-transition: all 0.1s ease-in-out;
            transition: all 0.1s ease-in-out;
        }

        .bordered td, .bordered th {
            border-left: 1px solid #ccc;
            border-top: 1px solid #ccc;
            padding: 2px;
            text-align: center;
        }

        .bordered th {
            background-color: #dce9f9;
            background-image: -webkit-gradient(linear, left top, left bottom, from(#ebf3fc), to(#dce9f9));
            background-image: -webkit-linear-gradient(top, #ebf3fc, #dce9f9);
            background-image:    -moz-linear-gradient(top, #ebf3fc, #dce9f9);
            background-image:     -ms-linear-gradient(top, #ebf3fc, #dce9f9);
            background-image:      -o-linear-gradient(top, #ebf3fc, #dce9f9);
            background-image:         linear-gradient(top, #ebf3fc, #dce9f9);
            -webkit-box-shadow: 0 1px 0 rgba(255,255,255,.8) inset;
            -moz-box-shadow:0 1px 0 rgba(255,255,255,.8) inset;
            box-shadow: 0 1px 0 rgba(255,255,255,.8) inset;
            border-top: none;
            text-shadow: 0 1px 0 rgba(255,255,255,.5);
        }

        .bordered td:first-child, .bordered th:first-child {
            border-left: none;
        }

        .bordered th:first-child {
            -moz-border-radius: 1px 0 0 0;
            -webkit-border-radius: 1px 0 0 0;
            border-radius: 1px 0 0 0;
        }

        .bordered th:last-child {
            -moz-border-radius: 0 1px 0 0;
            -webkit-border-radius: 0 1px 0 0;
            border-radius: 0 1px 0 0;
        }

        .bordered th:only-child{
            -moz-border-radius: 1px 1px 0 0;
            -webkit-border-radius: 1px 1px 0 0;
            border-radius: 1px 1px 0 0;
        }

        .bordered tr:last-child td:first-child {
            -moz-border-radius: 0 0 0 1px;
            -webkit-border-radius: 0 0 0 1px;
            border-radius: 0 0 0 1px;
        }

        .bordered tr:last-child td:last-child {
            -moz-border-radius: 0 0 1px 0;
            -webkit-border-radius: 0 0 1px 0;
            border-radius: 0 0 1px 0;
        }
      </style>
    </head>"""
    return head
 
# getEslList()

day_start = '2024-03-12 00:00:00.000'
day_end = '2024-05-13 00:00:00.000'

# genHtmlFile('eslworking0509.log','uplink04232.log',[],day_start,day_end)
genHtmlFile('eslworking.log',[],day_start,day_end)