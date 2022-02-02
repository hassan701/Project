function deleteOrder(orderId) {
  fetch("/delete_order", {
    method: "POST",
    body: JSON.stringify({ orderid: orderId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function deleteitem(itemId) {
  fetch("/delete_item", {
    method: "POST",
    body: JSON.stringify({ itemId: itemId }),
  }).then((_res) => {
    window.location.href = "/Data";
  });
}


function deleteemployee(employId) {
  fetch("/delete_employee", {
    method: "POST",
    body: JSON.stringify({ employId: employId }),
  }).then((_res) => {
    window.location.href = "/employee";
  });
}