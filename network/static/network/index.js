document.addEventListener('DOMContentLoaded',function(){

    document.querySelector('.div_add_post').style.display = 'none'
    
    
    document.querySelector('#new_post_button').onclick = ()=>{
        document.querySelector('.div_add_post').style.display = 'block'
        
    }

    const div = document.querySelectorAll('#div_update_description')
    div.forEach(element => {
        element.style.display = 'none'
    });
    

    const edit = document.querySelectorAll('#edit_button')
    edit.forEach(button =>{
        button.onclick = ()=>{
            const postId = button.getAttribute('div-id')
            console.log(postId);
            document.querySelector('.div_update_description_' + postId).style.display = 'block'
            
        }
    })

})