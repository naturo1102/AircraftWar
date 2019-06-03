Page({
  onTap:function(event){
    // wx.navigateTo({
    //   url: '../posts/post',
    // })
    // wx.redirectTo({
    //   url: '../posts/post',
    //   success: function(res) {},
    //   fail: function(res) {},
    //   complete: function(res) {},
    // })
    wx.switchTab({
      url: "../posts/post"
    });
  }
})