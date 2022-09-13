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
            method:'POST',
            headers: {'Content-Type': 'application/json',},
            body: JSON.stringify ({
                post: `${posts.id}`
                // post: 'aaaaaa'
            })
        })
    }


})