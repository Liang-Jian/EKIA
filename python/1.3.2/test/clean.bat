net stop "Hanshow sevice"
net stop "Hanshow web sevice"

rm log\*
rm db.sqlite

net start "Hanshow sevice"
net start "Hanshow web sevice"
