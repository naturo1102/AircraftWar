var postsData = require('../../../data/posts-data.js')
var app = getApp();
Page({
  /**
   * 页面的初始数据
   */
  data: {
    isplayingmusic: false,
    collected:'',
    
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    var postId = options.id;
    this.data.currentPostId = postId;
    var postData = postsData.postList[postId];
    //this.data.postsData = postData; 
    this.setData({
      postData: postData
    });

    var postsCollected = wx.getStorageSync('posts_collected')
    if (postsCollected) {
      var postCollected = postsCollected[postId]
      this.setData({
        collected: postCollected
      })
    } else {
      var postsCollected = {};
      postsCollected[postId] = false;
      wx.setStorageSync('posts_collected', postsCollected)
    }
    if (app.globalData.global_isPlayingMusic && app.globalData.global_currentMusicPostId == postId){
      // this.data.isplayingmusic =true;
      this.setData({
        isplayingmusic:true
        })
    }
    this.setMusicMonitor();
  },
  setMusicMonitor:function(){
    var that = this;
    wx.onBackgroundAudioPlay(function () {
      that.setData({
        isplayingmusic: true
      })
      app.globalData.global_isPlayingMusic = true;
      app.globalData.global_currentMusicPostId = that.data.currentPostId;
    })
    wx.onBackgroundAudioPause(function () {
      that.setData({
        isplayingmusic: false
      })
      app.globalData.global_isPlayingMusic = false;
      app.globalData.global_currentMusicPostId =null;
    })
  },
  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function() {

  },
  onCollectionTap: function(event) {
    /* if(this.collected){
       this.setData({collected:false})
       console.log("jinru")
     }
     else
       this.setData({collected:true})
     console.log("sdsf")*/
    var postsCollected = wx.getStorageSync('posts_collected');
    var postCollected = postsCollected[this.data.currentPostId];
    postCollected = !postCollected
    postsCollected[this.data.currentPostId] = postCollected;
    wx.setStorageSync('posts_collected', postsCollected)
    this.setData({
      collected: postCollected
    })
    wx.showToast({
      title: postCollected ? '收藏成功' : '取消成功',
      duration: 1000,
      icon: "success"
    })
  },
  onShareTap: function(event) {
    var itemList = [
      "分享给微信好用",
      "分享到朋友圈",
      "分享到QQ",
      "分享到微博"
    ]
    wx.showActionSheet({
      itemList: itemList,
      itemColor: "#405f80",
      success: function(res) {
        // res.canel 用户是否取消
        //res.tapIndex 数组中元素的顺序
        wx.showModal({
          title: itemList[res.tapIndex],
          content: "小程序暂时不支持该功能",
        })
      }
    })
  },
  onMusicTap: function(event) {
    var currentPostId = this.data.currentPostId;
    var isplayingmusic = this.data.isplayingmusic;
    var postDataMusic = postsData.postList[currentPostId];
    if (isplayingmusic) {
      wx.pauseBackgroundAudio();
      this.setData({
        isplayingmusic: false
      })
    } else {
      wx.playBackgroundAudio({
        dataUrl: postDataMusic.music.dataUrl,
        title: postDataMusic.music.title,
        coverImgUrl: postDataMusic.music.coverImgUrl
      })
      this.setData({
        isplayingmusic: true
      })
    }
  }
})