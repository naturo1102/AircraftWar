// pages/movies/more-movies/more-movies.js
var app = getApp();
var util = require('../../../utils/util.js');
Page({

  /**
   * 页面的初始数据
   */
  data: {
    movies:{},
    navigateTitle: '',
    requestUrl:'',
    totalCount:0,
    isEmpty:true
    },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var category = options.category;
    this.data.navigateTitle = category;
    var dataUrl = "";
    switch (category) {
      case "正在热映":
        dataUrl = app.globalData.WangShuWen + "/getHotMovie";
        break;
      case "热门推荐":
        dataUrl = app.globalData.WangShuWen + "/getHotMovie";
        break;
      case "豆瓣Top250":
        dataUrl = app.globalData.WangShuWen + "/getTopMovie";
        break;
    }
    this.data.requestUrl =dataUrl;
    util.http(dataUrl,this.callBack)
  },
  callBack: function (moviesList){
    console.log(moviesList);
    var movies = [];
    for (var idx in moviesList.data.subjects) {
      var subject = moviesList.data.subjects[idx];
      var title = subject.title;
      if (title.length >= 6) {
        title = title.substring(0, 6) + "...";
      }
      var temp = {
        stars: util.convertToStarsArray(subject.rating.stars),
        title: title,
        average: subject.rating.average,
        coverageUrl: subject.images.large,
        movieId: subject.id
      }
      movies.push(temp)
    }
    var totalMovies={}
    if(!this.data.isEmpty){
      totalMovies =this.data.movies.concat(movies);
    }
    else{
      totalMovies =movies;
      this.data.isEmpty=false;
    }
    this.setData({
      movies: totalMovies
    });
    this.data.totalCount += 10;
    wx.hideNavigationBarLoading();
    wx.stopPullDownRefresh()
  },
  onReady: function (event) {
    wx.setNavigationBarTitle({
      title: this.data.navigateTitle,
    }),
      wx.setNavigationBarColor({
        frontColor: '#ffffff',
        backgroundColor: '#b491f6',
        animation: {
          duration: 400,
          timingFunc: 'easeInOut'
        }
      })

  },
  onScrollLower:function(event){
    console.log("加载更多");
    var nextUrl = this.data.requestUrl+"?start"+this.data.totalCount+"&count=10";
    util.http(nextUrl, this.callBack)
    wx.showNavigationBarLoading();
  } ,
  onPullDownRefresh: function (event) {
    var refreshUrl = this.data.requestUrl + "?start=0&count=20";
    this.data.movies={};
    this.data.isEmpty =true;
    util.http(refreshUrl,this.callBack)
    wx.showNavigationBarLoading()
  }
})