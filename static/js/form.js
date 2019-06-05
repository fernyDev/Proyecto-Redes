$(document).ready(function(){
    $("#BUSCAR").on('submit',function(event){//id porque ya no es un solo formulario
    
        $.ajax({
            data : {
                name : $('#PathInput').val()    
            },
            type : 'POST',
            url : '/process'
        })
        .done(function(data){
            if(data.error){
                $('#errorAlert').text(data.error).show();
                $('#successAlert').hide();
            }
            else{
                text = ""
                console.log(data.cosa.length)
                for (i = 0 ; i < data.cosa.length ; i++){
                    text = text.concat(data.cosa[i]);
                }
                $('#successAlert').html(text);
                $('#successAlert').show();
                //$('#successAlert').text(data.name).show();
                $('#errorAlert').hide();
            }
        
        });
        
        event.preventDefault()
        
    });
//hacer lo mismo para enviar y descargar... que lean del id PathInput




	
});
