
  $(document).ready(function () {
  $image_crop = $("#user_profile_image").croppie({
  enableExif: false,
  viewport: {
  width: 289,
  height: 289,
  type: "square",
  },
  boundary: {
  width: 400,
  height: 400,
  },
  enableOrientation: false,
  });
  $("#user_Image").on("change", function () {
  var set_status = true;
  var reader = new FileReader();
  var fi = document.getElementById('user_Image');
  if (fi.files.length > 0) {
  for (var i = 0; i <= fi.files.length - 1; i++) {
  
  var fsize = fi.files.item(i).size;
  // console.log(fsize)
  var file = Math.round((fsize / 1024));
  console.log(file);
  if (file > 3072) {
  
  alert("Image is too Big, please select a image less than 3MB size.");
  }
  else
  {
  reader.onload = function (event) {
  var image = new Image();
  image.src = event.target.result;
  //Validate the File Height and Width.
  image.onload = function () {
  var height = this.height;
  var width = this.width;
  if (height >= 289 && width >= 289) {
  $image_crop
  .croppie("bind", {
  url: event.target.result,
  })
  .then(function () {
  console.log("jQuery bind complete");
  });
  $("#uploaduserimageModal").modal("show");
  } else {
  set_status = false;
  alert("Please select image greater that 289*289px.");
  }
  };
  };
  
  }
  
  }
  }
  if (set_status) {
  reader.readAsDataURL(this.files[0]);
  }
  });
  $(".crop_image_edit").click(function (event) {
  $(".crop_image_edit").html("Image Uploading");
  $(".crop_image_edit").attr("disabled", true);
  $image_crop
  .croppie("result", {
  type: "canvas",
  size: "viewport",
  })
  .then(function (response) {
  $(".crop_image_edit").html("Image Upload");
  $(".crop_image_edit").attr("disabled", false);
  $("#save_profile_image").val(response);

  $("#uploaduserimageModal").modal("hide");
  });
  });
  });



