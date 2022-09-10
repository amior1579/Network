document.addEventListener('DOMContentLoaded',function(){

    document.querySelector('.div_add_post').style.display = 'none'
    
    document.querySelector('#new_post_button').onclick = ()=>{
        document.querySelector('.div_add_post').style.display = 'block'
        
    }
    
    const div = document.querySelectorAll('#div_update_description')
    div.forEach(element => {
        element.style.display = 'none'
    });

    fetch(`/posts`)
    .then(response => response.json())
    .then(json_posts =>{
        json_posts.forEach(posts =>{
            console.log(posts);


            const edit = document.querySelector(`#edit_button_${posts.id}`)
            edit.addEventListener('click', ()=> edit_post(posts))


            // const like = document.querySelector(`#like_count_${posts.id}`)
            // edit.addEventListener('click', ()=> like_post(posts))

            
            

            // const edit = document.querySelectorAll('#edit_button')
            // edit.forEach(button =>{
            //     button.onclick = ()=>{
            //         const postId = button.getAttribute('div-id')
            //         console.log(postId);
            //         document.querySelector('.div_update_description_' + postId).style.display = 'block'
                    
            //         const description = document.querySelector('#post_description_' + postId)
            //         const inner = description.innerHTML
            //         console.log(inner);

            //         const form_update = document.querySelector('#form_update')
            //         form_update.value = inner
            //         console.log(form_update);

                    
            //         // edit_post(postId)
            //     }
            // }) 
        })
    })

    function edit_post(posts){
        document.querySelector(`.div_update_description_${posts.id}`).style.display = 'block'
        // document.querySelector(`#form_update_description_${posts.id}`).value = document.querySelector(`#post_description_${posts.id}`).innerHTML
        console.log(posts.id);

        const edit = document.querySelector(`#submit_button_${posts.id}`)
        edit.addEventListener('click', ()=>{
            console.log(edit);

            fetch(`/posts/${posts.id}`,{
                method:'PUT',
                headers: { "Content-Type": "application/json"},
                body: JSON.stringify({
                    // description: document.querySelector(`#form_update_description_${posts.id}`).value,
                    id: 22,
                    post_title: "dfv",
                    post_description: "vjbgygvgdfv",
                    post_date: "2022-09-10T16:06:33.907440Z",
                    like_count: 0,
                    post_uesr: 5,
                    post_likes: []

                })
            })
            return false
            // console.log(description);
        })

    }

    // function like_post(posts){
    //     console.log(posts.id);
    // }




})