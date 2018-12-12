jQuery(function(){
    $ = jQuery;
    $(window).load( function() {
        $('.external-link').unbind('click');    
    });
    //main menu
    $("#lib_banner_menu ul").singlePageNav({offset: $('#lib_banner_menu').outerHeight()});
    //banner slide
    $('.banner').unslider({fluid: true});
    $(window).on("load scroll resize", function(){
        banner_height = ($(document).width()/1920) * 760;
        $('.banner').height(banner_height);
        $('.banner ul li').height(banner_height);
        if(banner_height > 250){
            caption_margin_top = (banner_height-100)/2;
            $('.banner .slide_caption:hidden').show();
            $('.banner .slide_caption').css({"margin-top":caption_margin_top});
        }else{
            $('.banner .slide_caption').hide();
        }
        $("#lib_banner_slide > ul > li").css({"background-size":"cover"});
    });
    //about icon
    $(window).on("load scroll resize", function(){
        about_wap_width = $(".about_icon").width();
        about_icon_padding_left = (about_wap_width/100)*30;
        about_icon_width = (about_wap_width/100)*40;
        about_icon_size = (about_icon_width/100)*50;
        about_icon_padding_top = (about_icon_width/100)*25;
        $(".about_icon .imgwap").css({
                                                    'margin-left': about_icon_padding_left,
                                                    'width': about_icon_width,
                                                    'height': about_icon_width,
                                                    });
        $("#lib_about .about_icon .imgwap i").css({
                                                                                    "font-size":about_icon_size,
                                                                                    "padding-top":about_icon_padding_top,
                                                                                  });
        $(".about_icon p").css({
                                            'padding-left': "10%",
                                            'padding-right': "10%",
                                            });
    });
	
    //about textimonial
    $.current_testimonial = $("div.testimonial_text").first() ;
    $("div.testimonial_text").hide();
    $.current_testimonial.show();
    $(window).on("load scroll resize", function(){
        testimonial_child_height = $(".testimonial_text").height();
        $("#testimonial_text_wap").height(testimonial_child_height);
        $(".pre_next_wap").height(testimonial_child_height);
    });
    $("#prev_testimonial").click(function(){
        $.current_testimonial.effect("fade",{},200,function(){
                $.current_testimonial_prev = ($.current_testimonial.index() == 0) ? $(".testimonial_text").last() : $.current_testimonial.prev() ;
                $.current_testimonial_prev.fadeIn();
                $.current_testimonial = $.current_testimonial_prev;
        });
        return false;
    });
    $("#next_testimonial").click(function(){
        $.current_testimonial.effect("fade",{},200,function(){
                $.current_testimonial_next = ($.current_testimonial.index() == $(".testimonial_text").last().index() ) ? $(".testimonial_text").first() : $.current_testimonial.next() ;
                $.current_testimonial_next.fadeIn();
                $.current_testimonial = $.current_testimonial_next;
        });
        return false;
    });
    //event
    $(".event_box_img").load(function(){
        img_height = $(this).height();
        $(this).parent(".event_box_wap").height(img_height);
    });
    $(window).on("load resize", function(){
        img_height = $(".event_box_img").height();
        if($(window).width()>550){
            $(".event_box_wap").height(img_height);
            $(".event_box_wap").each(function(){
                total_height = $(this).children(".event_box_caption").outerHeight();
                header_height = $(this).children(".event_box_caption").children("h1").outerHeight();
                admin_height = $(this).children(".event_box_caption").children("p").eq(0).outerHeight();
                paragraph_height = $(this).children(".event_box_caption").children("p").eq(1).outerHeight();
                hide_paragraph_height = header_height + admin_height + 10 ;
                $(this).children(".event_box_caption").css({"top": "-" + hide_paragraph_height + "px"});
            });
        }else{
            $(".event_box_wap").height(img_height);
            $(".event_box_wap").each(function(){
                total_height = $(this).children(".event_box_caption").outerHeight();
                header_height = $(this).children(".event_box_caption").children("h1").outerHeight();
                admin_height = $(this).children(".event_box_caption").children("p").eq(0).outerHeight();
                paragraph_height = $(this).children(".event_box_caption").children("p").eq(1).outerHeight();
                hide_paragraph_height = header_height + admin_height + 10 ;
                $(this).height(total_height+img_height);
                $(this).children(".event_box_caption").css({"top": "0px"});
            });
        }
    });
    $(".event_box_wap").hover(function(){
        if($(window).width()>550){
            total_height = $(this).children(".event_box_caption").outerHeight();
            header_height = $(this).children(".event_box_caption").children("h1").outerHeight();
            admin_height = $(this).children(".event_box_caption").children("p").eq(0).outerHeight();
            paragraph_height = $(this).children(".event_box_caption").children("p").eq(1).outerHeight();
            hide_paragraph_height = header_height + admin_height + paragraph_height + 10 ;
            $(this).children(".event_box_caption").stop().animate({"top": "-" + hide_paragraph_height + "px"});
        }
    },function(){
        if($(window).width()>550){
            total_height = $(this).children(".event_box_caption").outerHeight();
            header_height = $(this).children(".event_box_caption").children("h1").outerHeight();
            admin_height = $(this).children(".event_box_caption").children("p").eq(0).outerHeight();
            paragraph_height = $(this).children(".event_box_caption").children("p").eq(1).outerHeight();
            hide_paragraph_height = header_height + admin_height + 10 ;
            $(this).children(".event_box_caption").stop().animate({"top": "-" + hide_paragraph_height + "px"});
        }
    });
    //mobile menu and desktop menu
    $("#lib_mobile_menu").css({"right":-1500});
    $("#mobile_menu").click(function(){
            $("#lib_mobile_menu").show();
            $("#lib_mobile_menu").animate({"right":0});
            return false;
    });
    $(window).on("load resize", function(){
            if($(window).width()>768){
                $("#lib_mobile_menu").css({"right":-1500});
            }
    });

    jQuery.fn.anchorAnimate = function(settings) {
        settings = jQuery.extend({
            speed : 1100
        }, settings);	
        return this.each(function(){
            var caller = this
            $(caller).click(function (event){
                event.preventDefault();
                var locationHref = window.location.href;
                var elementClick = $(caller).attr("href");
                var destination = $(elementClick).offset().top - $('#lib_banner_menu').outerHeight() ;
                $("#lib_mobile_menu").animate({"right":-1500});
                $("#lib_mobile_menu").fadeOut() ;
                $("html,body").css({"overflow":"auto"});
                $("html,body").stop().animate({ scrollTop: destination}, settings.speed, function(){
                    // Detect if pushState is available
                    if(history.pushState) {
                        history.pushState(null, null, elementClick);
                    }
                });
                return false;
            });
        });
    }
    //animate scroll function calll
    $("#lib_mobile_menu a").anchorAnimate();    
    //about
    $(document).scroll(function(){
        document_top = $(document).scrollTop();
        event_wapper_top = $("#lib_about").position().top - $('#lib_banner_menu').outerHeight();
        if(document_top<event_wapper_top){
            degree = (360/event_wapper_top)*(document_top);
            event_animate_num = event_wapper_top - document_top;
            event_animate_alpha = (1/document_top)*(event_wapper_top);
            $("#lib_about .imgwap").css({
                        '-webkit-transform': 'rotate(' + degree + 'deg)',
                        '-moz-transform': 'rotate(' + degree + 'deg)',
                        '-ms-transform': 'rotate(' + degree + 'deg)',
                        '-o-transform': 'rotate(' + degree + 'deg)',
                        'transform': 'rotate(' + degree + 'deg)',
            });
            $("#lib_about .about_icon").css({
                        'opacity':event_animate_alpha
            });
        }else{
            $("#lib_about .imgwap").css({
                        '-webkit-transform': 'rotate(' + 360 + 'deg)',
                        '-moz-transform': 'rotate(' + 360 + 'deg)',
                        '-ms-transform': 'rotate(' + 360 + 'deg)',
                        '-o-transform': 'rotate(' + 360 + 'deg)',
                        'transform': 'rotate(' + 360 + 'deg)',
            });
            $("#lib_about .about_icon").css({
                        'opacity':1
            });
        }
    });
    //events
    //event
    $(document).scroll(function(){
        document_top = $(document).scrollTop();
        event_wapper_top = $("#lib_events").position().top - $('#lib_banner_menu').outerHeight();
        if(document_top<event_wapper_top){
            event_animate_num = event_wapper_top - document_top;
            event_animate_alpha = (1/event_wapper_top)*(document_top);
            $("#lib_events .event_animate_left").css({'left': -event_animate_num,'opacity':event_animate_alpha});
            $("#lib_events .event_animate_right").css({'left':event_animate_num,'opacity':event_animate_alpha});
        }else{
            $("#lib_events .event_animate_left").css({'left': 0,'opacity':1});
            $("#lib_events .event_animate_right").css({'left':0,'opacity':1});
        }
    }); 
});