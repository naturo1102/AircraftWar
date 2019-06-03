var util = require('../../utils/util.js');
var app =getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {
    inTheaters:{},
    comingSoon:{},
    top250:{}
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (event) {
    var inTheatersUrl = app.globalData.WangShuWen+"/getHotMovie"+"?start=0&count=3";
    var comingSoonUrl = app.globalData.WangShuWen + "/getHotMovie"+"?start=0&count=3";
    var top250Url = app.globalData.WangShuWen + "/getTopMovie"+"?start=0&count=3";
    this.getMovieListData(inTheatersUrl,"inTheaters","正在热映");
    this.getMovieListData(comingSoonUrl,"comingSoon","热门推荐");
    this.getMovieListData(top250Url,"top250","豆瓣Top250");

  },
  getMovieListData: function (url, setteKey, catgoryTitle){
     var that = this;
     wx.request({
       url: url,
       header: {
         "Conten-Type": "application"
       },
       method: 'GET',
       dataType: 'json',
       responseType: 'text',
       success: function (res) {
         that.processData(res.data.data, setteKey, catgoryTitle)
       },
       fail: function (res) {
         console.log("failed")
       },
     })
   },
  processData: function (moviesList, setteKey, catgoryTitle){
   var movies =[];
   for(var idx in moviesList.subjects){
    var subject = moviesList.subjects[idx];
    var title =subject.title;
    if(title.length>=6){
      title = title.substring(0,6)+"...";
    }
    var temp={
      stars:util.convertToStarsArray(subject.rating.stars),
      title:title,
      average:subject.rating.average,
      coverageUrl:subject.images.large,
      movieId:subject.id
    }
    movies.push(temp)
   }
   var readyData={};
   readyData[setteKey] ={
     movies:movies,
     catgoryTitle: catgoryTitle

   }
   this.setData(
    //  movies:movies
    readyData
   );
  },
  onMoreTap:function(event){
    var category = event.currentTarget.dataset.category;
    wx.navigateTo({
      url: 'more-movies/more-movies?category='+category
    })
  }
})
