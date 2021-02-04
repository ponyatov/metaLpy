sio = io();

sio.on('connect',()=>{
    console.log('sio','connect')
    $('#localtime').addClass('online').removeClass('offline')
})

sio.on('disconnect',()=>{
    console.log('sio','disconnect')
    $('#localtime').addClass('offline').removeClass('online')
})

LOCALTIME_REFRESH = 60e3

sio.on('localtime',(msg)=>{
    // console.log('sio','localtime',msg)
    $('#localtime').text(msg.date+" | "+msg.time)
    if (msg.refresh) LOCALTIME_REFRESH = msg.refresh
    // setTimeout(()=>{sio.emit('localtime')},LOCALTIME_REFRESH)
})
