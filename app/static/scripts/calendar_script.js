var dias_selecionados = []
$(".days").children().click(function() {
    console.log("aaaa")
    var myNumber = 0
      if($(this).children().length > 0) {
          myNumber = $(this).children().text()
            console.log(myNumber)
            $(this).html(myNumber)
            array_remove_index_by_value(dias_selecionados,myNumber)
            console.log(dias_selecionados)
        }
        else {
            myNumber = $(this).text()
            console.log(myNumber)
            $(this).html("<span class='active'>" + myNumber + "</span>")
            dias_selecionados.push(myNumber)
            console.log(dias_selecionados) 
        }
    })
  function array_remove_index_by_value(arr, item)
  {
    for (var i = arr.length; i--;)
    {
      if (arr[i] === item) {arr.splice(i, 1);}
    }
  }