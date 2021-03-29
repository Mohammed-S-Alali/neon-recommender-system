var user_id; 

$(function() {
  // Button will be disabled until we type anything inside the input field
  const source = document.getElementById('autoComplete');
  const inputHandler = function(e) {
    if(e.target.value==""){
      $('.movie-button').attr('disabled', true);
    }
    else{
      $('.movie-button').attr('disabled', false);
    }
  }
  source.addEventListener('input', inputHandler);

  $('.movie-button').on('click',function(){
    var my_api_key = 'ccd8edded74fa516c4913c6bf451d21f';
    var title = $('.movie').val();

    var user_id_dl = document.getElementById('user_id_dl');
    var user_id_value = user_id_dl.options[user_id_dl.selectedIndex].value

    if(user_id_value!=''){
          user_id = user_id_value;
        }
        else if(user_id_value=='None'){
          user_id = 1847;
        }
        else if(user_id_value == ''){
          user_id = undefined;
        }
      
    if ((title == null || title.trim() === '' || title=="") && user_id == undefined) {
      $('.results').css('display','none');
      $('.fail').css('display','none');
      $('.fail_1').css('display','none');
      $('.fail_2').css('display','none');
      $('.fail_3').css('display','block');
    }
    else if ((title == null || title.trim() === '' || title=="") && user_id != undefined) {
      $('.results').css('display','none');
      $('.fail').css('display','none');
      $('.fail_1').css('display','none');
      $('.fail_2').css('display','block');
      $('.fail_3').css('display','none');
    }
    else if(!(title == null || title.trim() === '' || title=="") && user_id == undefined){
      $('.results').css('display','none');
      $('.fail').css('display','block');
      $('.fail_1').css('display','none');
      $('.fail_2').css('display','none');
      $('.fail_3').css('display','none');
    }
    else if(!(title == null || title.trim() === '' || title=="") && user_id != undefined){
      load_details(my_api_key,title,user_id);
    }
  });
});


// will be invoked when clicking on the recommended movies
function recommendcard(e){
  var my_api_key = 'ccd8edded74fa516c4913c6bf451d21f';
  var title = e.getAttribute('title'); 
  load_details(my_api_key,title,user_id);
}

// get the basic details of the movie from the API (based on the name of the movie)
function load_details(my_api_key,title,user_id){
  $.ajax({
    type: 'GET',
    url:'https://api.themoviedb.org/3/search/movie?api_key='+my_api_key+'&query='+title,

    success: function(movie){
      if(movie.results.length<1){
        $('.fail').css('display','none');
        $('.fail_1').css('display','block');
        $('.fail_2').css('display','none');
        $('.fail_3').css('display','none');
        $('.results').css('display','none');
        $("#loader").delay(500).fadeOut();
      }
      else{
        $("#loader").fadeIn();
        $('.fail').css('display','none');
        $('.fail_1').css('display','none');
        $('.fail_2').css('display','none');
        $('.fail_3').css('display','none');
        $('.results').delay(500).css('display','block');
        var movie_id = movie.results[0].id;
        var movie_title = title;
        movie_recs(movie_title,movie_id,my_api_key,user_id);
      }
    },
    error: function(){
      alert('Invalid Request');
      $("#loader").delay(500).fadeOut();
    },
  });
}

// passing the movie name to get the similar movies from python's flask
function movie_recs(movie_title,movie_id,my_api_key,user_id){
  $.ajax({
    type:'POST',
    url:"/similarity",
    data:{'name':movie_title,'user_id':user_id},
    success: function(recs){
      if(recs=="Sorry! The movie you requested is not in our database. Please check the spelling or try with some other movies"){
        $('.fail').css('display','none');
        $('.fail_1').css('display','block');
        $('.fail_2').css('display','none');
        $('.fail_3').css('display','none');
        $('.results').css('display','none');
        $("#loader").delay(500).fadeOut();
      }
      else{
        $('.fail').css('display','none');
        $('.fail_1').css('display','none');
        $('.fail_2').css('display','none');
        $('.fail_3').css('display','none');
        $('.results').css('display','block');
        var movie_arr = []
        recs = recs.split('_');
        recs.forEach(element => {
          movie_arr.push(element.split('---'));
        });

        var arr = [];

        movie_arr.forEach(element => {
                  arr.push(element);
        });

        get_movie_details(movie_id,my_api_key,arr,movie_title);
      }
    },
    error: function(){
      alert("Please try again!");
      $("#loader").delay(500).fadeOut();
    },
  }); 
}

// get all the details of the movie using the movie id.
function get_movie_details(movie_id,my_api_key,arr,movie_title) {
  $.ajax({
    type:'GET',
    url:'https://api.themoviedb.org/3/movie/'+movie_id+'?api_key='+my_api_key,
    success: function(movie_details){
      show_details(movie_details,arr,movie_title,my_api_key,movie_id);
    },
    error: function(){
      alert("API Error!");
      $("#loader").delay(500).fadeOut();
    },
  });
}

// passing all the details to python's flask for displaying and scraping the movie reviews using imdb id
function show_details(movie_details,arr,movie_title,my_api_key,movie_id){
  var imdb_id = movie_details.imdb_id;
  var poster = 'https://image.tmdb.org/t/p/original'+movie_details.poster_path;
  var overview = movie_details.overview;
  var genres = movie_details.genres;
  var rating = movie_details.vote_average;
  var vote_count = movie_details.vote_count;
  var release_date = new Date(movie_details.release_date);
  var runtime = parseInt(movie_details.runtime);
  var status = movie_details.status;
  var genre_list = []
  for (var genre in genres){
    genre_list.push(genres[genre].name);
  }
  var my_genre = genre_list.join(", ");
  if(runtime%60==0){
    runtime = Math.floor(runtime/60)+" hour(s)"
  }
  else {
    runtime = Math.floor(runtime/60)+" hour(s) "+(runtime%60)+" min(s)"
  }
  arr_poster = []
  
   arr.forEach(element => {
     arr_poster.push(get_movie_posters(element,my_api_key));
   });
  
  movie_cast = get_movie_cast(movie_id,my_api_key);
  
  ind_cast = get_individual_cast(movie_cast,my_api_key);
  
  details = {
    'title':movie_title,
      'cast_ids':JSON.stringify(movie_cast.cast_ids),
      'cast_names':JSON.stringify(movie_cast.cast_names),
      'cast_chars':JSON.stringify(movie_cast.cast_chars),
      'cast_profiles':JSON.stringify(movie_cast.cast_profiles),
      'cast_bdays':JSON.stringify(ind_cast.cast_bdays),
      'cast_bios':JSON.stringify(ind_cast.cast_bios),
      'cast_places':JSON.stringify(ind_cast.cast_places),
      'imdb_id':imdb_id,
      'poster':poster,
      'genres':my_genre,
      'overview':overview,
      'rating':rating,
      'vote_count':vote_count.toLocaleString(),
      'release_date':release_date.toDateString().split(' ').slice(1).join(' '),
      'runtime':runtime,
      'status':status,
      'rec_movies_0':JSON.stringify(arr[0]),
      'rec_movies_1':JSON.stringify(arr[1]),
      'rec_movies_2':JSON.stringify(arr[2]),
      'rec_movies_3':JSON.stringify(arr[3]),
      'rec_movies_4':JSON.stringify(arr[4]),
      'rec_movies_5':JSON.stringify(arr[5]),
      'rec_posters_0':JSON.stringify(arr_poster[0]),
      'rec_posters_1':JSON.stringify(arr_poster[1]),
      'rec_posters_2':JSON.stringify(arr_poster[2]),
      'rec_posters_3':JSON.stringify(arr_poster[3]),
      'rec_posters_4':JSON.stringify(arr_poster[4]),
      'rec_posters_5':JSON.stringify(arr_poster[5])
  }

  $.ajax({
    type:'POST',
    data:details,
    url:"/recommend",
    dataType: 'html',
    complete: function(){
      $("#loader").delay(500).fadeOut();
    },
    success: function(response) {
      $('.results').html(response);
      $('#autoComplete').val('');
      $(window).scrollTop(0);
    }
  });
}

// get the details of individual cast
function get_individual_cast(movie_cast,my_api_key) {
    cast_bdays = [];
    cast_bios = [];
    cast_places = [];
    for(var cast_id in movie_cast.cast_ids){
      $.ajax({
        type:'GET',
        url:'https://api.themoviedb.org/3/person/'+movie_cast.cast_ids[cast_id]+'?api_key='+my_api_key,
        async:false,
        success: function(cast_details){
          cast_bdays.push((new Date(cast_details.birthday)).toDateString().split(' ').slice(1).join(' '));
          cast_bios.push(cast_details.biography);
          cast_places.push(cast_details.place_of_birth);
        }
      });
    }
    return {cast_bdays:cast_bdays,cast_bios:cast_bios,cast_places:cast_places};
  }

// getting the details of the cast for the requested movie
function get_movie_cast(movie_id,my_api_key){
    cast_ids= [];
    cast_names = [];
    cast_chars = [];
    cast_profiles = [];

    top_10 = [0,1,2,3,4,5,6,7,8,9];
    $.ajax({
      type:'GET',
      url:"https://api.themoviedb.org/3/movie/"+movie_id+"/credits?api_key="+my_api_key,
      async:false,
      success: function(my_movie){
        if(my_movie.cast.length>=10){
          top_cast = [0,1,2,3,4,5,6,7,8,9];
        }
        else {
          top_cast = [0,1,2,3,4];
        }
        for(var my_cast in top_cast){
          cast_ids.push(my_movie.cast[my_cast].id)
          cast_names.push(my_movie.cast[my_cast].name);
          cast_chars.push(my_movie.cast[my_cast].character);
          cast_profiles.push("https://image.tmdb.org/t/p/original"+my_movie.cast[my_cast].profile_path);
        }
      },
      error: function(){
        alert("Invalid Request!");
        $("#loader").delay(500).fadeOut();
      }
    });

    return {cast_ids:cast_ids,cast_names:cast_names,cast_chars:cast_chars,cast_profiles:cast_profiles};
  }

// getting posters for all the recommended movies
function get_movie_posters(arr,my_api_key){
  var arr_poster_list = []
  for(var m in arr) {
    $.ajax({
      type:'GET',
      url:'https://api.themoviedb.org/3/search/movie?api_key='+my_api_key+'&query='+arr[m],
      async: false,
      success: function(m_data){
        arr_poster_list.push('https://image.tmdb.org/t/p/original'+m_data.results[0].poster_path);
      },
      error: function(){
        alert("Invalid Request!");
        $("#loader").delay(500).fadeOut();
      },
    })
  }
  return arr_poster_list;
}
