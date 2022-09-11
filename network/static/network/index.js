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
        const form_update =  document.querySelector(`#form_update_description_${posts.id}`)
        form_update.innerHTML = document.querySelector(`#post_description_${posts.id}`).innerHTML
        console.log(posts.id);

        const edit = document.querySelector(`#submit_button_${posts.id}`)
        edit.addEventListener('click', ()=>{
            
            fetch(`/posts/${posts.id}`,{
                method:'PUT',
                body: JSON.stringify({
                    description: form_update.value,
              })
            })
  
            document.querySelector(`.div_update_description_${posts.id}`).style.display = 'none'
            document.querySelector(`#post_description_${posts.id}`).innerHTML = form_update.value
        })
    }

    // function like_post(posts){
    //     console.log(posts.id);
    // }




})