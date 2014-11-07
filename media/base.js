
function init(data, data2, data3, data4, data5, data6, data7)
{
	compile_templates();
	start_main();
	window[action + '_init'](data, data2, data3, data4, data5, data6, data7);
	activate_keyboard();
	$(window).unload(function()
	{
		unload_user();
	});
	last_y = 0;
	bottom = false;
	$(document).scroll(function()
	{
		scrollertimer();
	})
}

function start_main()
{
	t = template_main();
	$('body').html(t);
}

function main_init(threads)
{
	t = template_threads_top({auth:auth})
	$('body').html(t)
	threadlist = get_threadlist(threads);
	t = template_threads({threads:threadlist})
	$('#threadlist').html(t);
}

function ForumItem(id, name, activity)
{
	this.id = id;
	this.name = decode(name);
	this.activity = activity;
}

function compile_templates()
{
	template_main = Handlebars.compile($('#template_main').html());	
	template_threads_top = Handlebars.compile($('#template_threads_top').html());	
	template_threads = Handlebars.compile($('#template_threads').html());	
	template_thread_top = Handlebars.compile($('#template_thread_top').html());	
	template_new_thread = Handlebars.compile($('#template_new_thread').html());	
	template_posts = Handlebars.compile($('#template_posts').html());	
	template_post = Handlebars.compile($('#template_post').html());	
	template_new_poll = Handlebars.compile($('#template_new_poll').html());	
	template_poll = Handlebars.compile($('#template_poll').html());	
	template_results = Handlebars.compile($('#template_results').html());	
	template_options = Handlebars.compile($('#template_options').html());	
	template_user = Handlebars.compile($('#template_user').html());	
}

function activate_keyboard()
{

}

function ThreadItem(id, name, activity)
{
	this.id = id;
	this.name = decode(name);
	this.activity = activity;
}

function pretty_url()
{
	title = window.location['pathname'].replace(/%20/g, '-')
	window.history.pushState({"html":'',"pageTitle":''},"", '../..' + title);
}

function forum_init(forum, threads, id)
{
	forum_id = id;
	t = template_forum_top({forum:decode(forum)})
	$('body').html(t)
	threadlist = get_threadlist(threads);
	t = template_threads({threads:threadlist})
	$('#threadlist').html(t);
}

function get_threadlist(threads)
{
	threadlist = [];
	for(var i=0; i<threads.length; i++)
	{
		threadlist.push(new ThreadItem(threads[i][0], threads[i][1], threads[i][2]))
	}
	return threadlist;
}

function new_thread_init(forum)
{
	t = template_new_thread({forum:decode(forum)})
	$('body').html(t); 
	$('#name').focus();
	$('#name').width($('#content').width());
}

function PostItem(id, content, user, date, thumbed, num_thumbs)
{
	this.id = id;
	this.content = decode(content); 
	this.user = user;
	this.date = date;
	this.thumbed = thumbed;
	this.num_thumbs = num_thumbs;
}

function OptionItem(id, name)
{
	this.id = id;
	this.name = decode(name);
}

function thread_init(name, posts, id, options, mode, voted)
{
	thread_mode = mode[0];
	thread_name = decode(name[0]);
	thread_id = id
	t = template_thread_top({name:decode(name)});
	$('body').html(t);
	if(options !== 0 && !voted)
	{
		optionlist = []
		for(var i=0; i<options.length; i++)
		{
			optionlist.push(new OptionItem(options[i][0], options[i][1]))
		}
		t = template_poll({options:optionlist})
		$('#poll').html(t)
	}
	else if(options !== 0 && voted)
	{
		update_poll_results();
	}
	postlist = get_postlist(posts);
	t = template_posts({posts:postlist});
	$('#postlist').html(t);
	respondlist = [];
}

function get_postlist(posts)
{
	postlist = [];
	for(var i=0; i<posts.length; i++)
	{
		content = posts[i][1]
		content = content.replace(/\[cita\]/g, "<div class='outer_quote'><div class='quote'>")
		content = content.replace(/\[\/cita\]/g, "</div></div>")
		console.log('content: ' + content);
		postlist.push(new PostItem(posts[i][0], content, posts[i][2], posts[i][3], eval(posts[i][4]), posts[i][5]))
	}
	return postlist;
}

function ResultItem(id, name, votes)
{
	this.id = id;
	this.name = name;
	this.votes = votes;
}

function update_poll_results()
{
	$.get('/update_poll_results/',
    {
    	thread_id: thread_id,
        csrfmiddlewaretoken: csrf_token
    },
	function(data) 
	{
		if(data['status'] === 'ok')
		{
			results = []
			for(var i=0; i<data['results'].length; i++)
			{
				results.push(new ResultItem(data['results'][i][0], data['results'][i][1], data['results'][i][2]))
			}
			t = template_results({results:results});
			$('#poll').html(t)
		}
	});
}

function post_init(name, quotes)
{
	t = template_post({name:name});
	$('body').html(t);
	$('#content').html(decode(quotes))
	data = $('#content').val();
	$('#content').focus().val('').val(data)
}

function thumbs(el)
{
	if($(el).attr('src') === '/media/img/thumbs')
	{
		$(el).attr('src', '/media/img/thumbsup')
	}
	else
	{
		$(el).attr('src', '/media/img/thumbs')
	}
	id = $(el).parent().parent().parent().attr('id')
    $.get('/thumbs/',
    {
    	id: id,
    },
	function(data) 
	{
		num_thumbs = data['num_thumbs'];
		$('#num_thumbs_' + id).html('&nbsp;(' + num_thumbs + ')');
	});
}

function add_to_responses(el)
{
	id = $(el).parent().parent().parent().attr('id');
	if($(el).hasClass('respond'))
	{
		$(el).attr('class', 'respond_selected')
		respondlist.push(id)
	}
	else
	{
		$(el).attr('class', 'respond')
		var index = respondlist.indexOf(id);
		if (index > -1) 
		{
    		respondlist.splice(index, 1);
    	}
	}
	return false;
}

function goto_respond()
{
	s = '';
	for(var i=0; i<respondlist.length; i++)
	{
		s = s + '&respondlist=' + respondlist[i]
	}
	window.location = '/' + thread_id + '/responder?' + s
}

function new_poll_init()
{
	t = template_new_poll()
	$('body').html(t); 
	$('#name').focus()
	$('#name').width($('#content').width())
	num_options = 2;
}

function add_more_options()
{
	s = "<div class='v06'></div><input name='option" + (num_options + 1) + "' type='text'>"
	$('#options').append(s)
	num_options += 1;
}

function vote()
{
	id = $('input[name=poll]:checked').val()
	if(id !== undefined)
	{

	}
	$.post('/vote/',
    {
    	thread_id: thread_id,
    	option_id: id,
        csrfmiddlewaretoken: csrf_token
    },
	function(data) 
	{
		update_poll_results();
	});
}

function options_init()
{
	date = new Date().getTime()
	t = template_options({username:username, date:date});
	$('body').html(t)
	$('#avatar').change(function()
	{
		document.form.submit()
	})
}

var scrollertimer = (function()
{
	var timer;
	return function()
	{
		clearTimeout(timer);
		timer = setTimeout(function()
		{
			if(action == 'forum')
			{
				var y = window.scrollY;
				if(y > last_y)
				{
					if(inViewport($('#bottom')[0]))
					{
						if(bottom) return;
						load_more();
					}
				}
				last_y = y
			}
		}, 1000);
	}
})();

function load_more()
{
	bottom = true;
	if(action == 'forum')
	{
		$.get('/load_more_threads/',
	    {
	    	last_thread_id: $('.thread').last().attr('id'),
	    },
		function(data) 
		{
			bottom = false;

			threadlist = get_threadlist(data['threads']);
			t = template_threads({threads:threadlist});
			$('#threadlist').append(t);
		});
	}
}

function inViewport (el) {
    var rect = el.getBoundingClientRect();

    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) && /*or $(window).height() */
        rect.right <= (window.innerWidth || document.documentElement.clientWidth) /*or $(window).width() */
    );
}

function resize_videos()
{
    var $allVideos = $(".postblock iframe[src^='http://www.youtube.com'],#posts iframe[src^='http://player.vimeo.com'],#posts iframe[src^='http://www.dailymotion.com']"),
        $fluidEl = $(".postblock");
    $allVideos.each(function() 
    {
            $(this)
                    .data('aspectRatio', this.height / this.width)
                    .removeAttr('height')
                    .removeAttr('width');
    });
    $(window).resize(function() 
    {
            var newWidth = $fluidEl.width();
            $allVideos.each(function() 
            {
                    var $el = $(this);
                    $el
                            .width(newWidth)
                            .height(newWidth * $el.data('aspectRatio'));
            });
    }).resize();
}

function decode(s) 
{
	try
	{
  		return decodeURIComponent(escape(s));
	}
	catch(err)
	{

	}
}

function go_to_the_end()
{
	$('html, body').animate({scrollTop:$(document).height()}, 300);
}

function go_up()
{
	$('html,body').animate({scrollTop:0}, 300);
}

function user_init(username)
{
	t = template_user({username:username})
	$('body').html(t)
}