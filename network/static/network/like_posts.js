document.addEventListener('DOMContentLoaded',function(){

    fetch(`/posts`)
    .then(response => response.json())
    .then(json_posts =>{
        json_posts.forEach(posts =>{
            console.log(posts);
            console.log(posts.id);

            const like = document.querySelector(`#like_button_${posts.id}`)
            if(like){
                like.addEventListener('click', ()=> like_post(posts), false)
            }
        })
    })

    function like_post(posts){
        fetch('/like',{
            method:'PUT',
            headers: {'Content-Type': 'application/json',},
            body: JSON.stringify ({
                post: `${posts.id}`,
            })
        })

        const like =  document.querySelector(`#like_count_${posts.id}`)
        const like_num = parseInt(like.innerHTML)
        const like_button = document.querySelector(`#like_button_${posts.id}`)

        if(like_button.innerHTML == 'Like'){
            like.innerHTML = like_num + 1
            like_button.innerHTML = 'Unlike'
        }else {
            like_button.innerHTML = 'Like'
            like.innerHTML = like_num - 1
        }
    }


})