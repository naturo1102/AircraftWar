function convertToStarsArray(stars) {
  var num = stars.toString().substring(0, 1);
  var array = [];
  for (var i = 1; i <= 5; i++) {
    if (i <= num) {
      array.push(1);
    }
    else {
      array.push(0);
    }
  }
  return array;
}
function http(url,callBack) {
    wx.request({
      url: url,
      header: {
        "Conten-Type": ""
      },
      method: 'GET',
      dataType: 'json',
      responseType: 'text',
      success: function (res) {
        callBack(res.data);
      },
      fail: function (res) {
        console.log('error')
      },
    })
  }
module.exports = {
  convertToStarsArray: convertToStarsArray,
  http:http
}