document.addEventListener('DOMContentLoaded',function(){

    fetch(`/posts`)
    .then(response => response.json())
    .then(json_posts =>{
        json_posts.forEach(posts =>{
            console.log(posts);
            console.log(posts.id);

            const like = document.querySelector(`#like_button_${posts.id}`)
            like.addEventListener('click', ()=> like_post(posts))
            console.log(like);
            
        })
    })

    function like_post(posts){
        console.log(posts.id);

        fetch('/like',{
            method:'PUT',
            headers: {'Content-Type': 'application/json',},
            body: JSON.stringify ({
                post: `${posts.id}`,
                // post: 'aaaaaa'
            })

        })
        const like =  document.querySelector(`#like_count_${posts.id}`)
        console.log(parseInt(like.innerHTML));
        const like_num = parseInt(like.innerHTML)
        console.log(like_num);
        const like_button = document.querySelector(`#like_button_${posts.id}`)
        console.log(like_button.innerHTML);
        if(like_button.innerHTML == 'Like'){
            like.innerHTML = like_num + 1
            like_button.innerHTML = 'Unlike'
        }
        else {
            like_button.innerHTML = 'Like'
            like.innerHTML = like_num - 1
        }
        console.log(like_num + 1);
    }


})