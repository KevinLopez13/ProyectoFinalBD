const btnsEliminacion=document.querySelectorAll('.btnEliminar');

(function(){
    btnsEliminacion.forEach(btn => {
        btn.addEventListener('click', function(e){
            e.preventDefault();
            Swal.fire({
                title: "¿Eliminar el articulo?",
                showCancelButton: true,
                confirmButtonText: "Eliminar",
                confirmButtonColor: "#d33",
                backdrop: true,
                showLoaderOnConfirm:true,
                preConfirm:()=>{
                    location.href=e.target.href;
                    //console.log("Confirmado");
                },
                allowOutsideClick:()=>false,
                allowEscapeKey:()=>false
            })
        });
    });
})();