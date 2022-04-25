function deleteInfo(infoId) {
  fetch("/delete-info", {
    method: "POST",
    body: JSON.stringify({ infoId: infoId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
