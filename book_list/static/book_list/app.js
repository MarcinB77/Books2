  $(document).ready(function() {

  $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
    // gather all the inputs we will need:
    var Year_val = parseFloat(data[2]) ||  0.0;
    var Year_min = parseFloat($('#Year_min').val()) || 0;
    var Year_max = parseFloat($('#Year_max').val()) || Number.MAX_VALUE;

    var Pages_val = parseFloat(data[4]) ||  0.0;
    var Pages_min = parseFloat($('#Pages_min').val()) || 0;
    var Pages_max = parseFloat($('#Pages_max').val()) || Number.MAX_VALUE;


    // evaluate to true to filter in a row, or false to filter it out:
    var Year = (Year_val >= Year_min && Year_val <= Year_max);
    var Pages = (Pages_val >= Pages_min && Pages_val <= Pages_max);

    // combine the above evaluations for overall row filtering:
    return Year && Pages;
  });

  // Setup - add a text input to each footer cell
  $('#dataTable thead tr').clone(true).appendTo('#dataTable thead');
  $('#dataTable thead tr:eq(1) th').each( function (i) {
    var title = $(this).text();
    if(title==='Year' || title==='Pages') {
      $(this).html(`
        <div class='d-flex'>
          <input name=${title}_min id=${title}_min class='' type='number' min='0' placeholder='from' style='width: 80px;'/>
          <input name=${title}_max id=${title}_max class='ml-1' type='number' min='0' placeholder='to' style='width: 80px;'/>
        </div>
      `);

      $(`#${title}_min`, this).on('keyup change', function () {
        minInputValue = parseFloat($(this).val()) || 0;
        dataTable.draw();
      });

      $(`#${title}_max`, this).on('keyup change', function () {
        maxInputValue = parseFloat($(this).val()) || 0;
        dataTable.draw();
      });

    }
    else if(title==='Cover') {
     $(this).html(`
        <div class='d-flex'>
        </div>
      `);
    }
    else {
      $(this).html('<input type="text" placeholder="Search '+title+'" />');
      $('input', this).on('keyup change', function () {
        if (dataTable.column(i).search() !== this.value) {
          dataTable.column(i).search(this.value).draw();
        }
      });
    }
  });

  var dataTable = $('#dataTable').DataTable({
    orderCellsTop: true,
    paging: true,
    scrollX: 400,
    searching: true,
    // lengthMenu: true,
    dom: 'Blfrtip',
    buttons: [
      { extend: 'csv', className: 'mb-2 btn btn-sm btn-info'},
      { extend: 'excel', className: 'mb-2 btn btn-sm btn-info' },
      { extend: 'pdf', className: 'mb-2 btn btn-sm btn-info' },
      { extend: 'print', className: 'mb-2 btn btn-sm btn-info' },
    ]
  });

  $('#dataTable_wrapper .dataTables_length').css({ display: 'inline-flex', 'margin-left': '20px' })
});