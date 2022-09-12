document.addEventListener('DOMContentLoaded',function(){

    fetch(`/posts`)
    .then(response => response.json())
    .then(json_posts =>{
        json_posts.forEach(posts =>{
            console.log(posts);
            console.log(posts.id);

            const like = document.querySelector(`#like_button_${posts.id}`)
            like.onclick = ()=> like_post(posts)
            
        })
    })

    function like_post(posts){
        console.log(posts.id);
    }


})