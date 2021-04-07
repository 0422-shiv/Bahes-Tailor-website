

$(document).ready(function () {

$img_crop = $("#service_image_edit").croppie({

enableExif: false,
viewport: {
width: 341,
height: 405,
type: "square",
},
boundary: {
width: 464,
height: 464,
},
enableOrientation: false,
});
$("#id_edit_service_Image").on("change", function () {

var status = true;
var read = new FileReader();
var fi = document.getElementById('id_edit_service_Image');
if (fi.files.length > 0) {
for (var i = 0; i <= fi.files.length - 1; i++) {

var fsize = fi.files.item(i).size;
// console.log(fsize)
var file = Math.round((fsize / 1024));

if (file > 3072) {

alert("Image is too Big, please select a image less than 3MB size.");
}
else
{
read.onload = function (event) {
var img = new Image();

img.src = event.target.result;
//Validate the File Height and Width.
img.onload = function () {
var height = this.height;
var width = this.width;
if (height >= 405 && width >= 341) {
$img_crop
.croppie("bind", {
url: event.target.result,
})
.then(function () {
console.log("jQuery bind complete");
});

$("#uploadserviceimageModal_edit").modal("show");
$("#exampleModal-1").modal("hide");
} else {
status = false;
alert("Please select image greater than 341*405 px.");
}
};
};

}

}
}
if (status) {
read.readAsDataURL(this.files[0]);
}
});
$(".crop_image").click(function (event) {
$(".crop_image").html("Image Uploading");
$(".crop_image").attr("disabled", true);
$img_crop
.croppie("result", {
type: "canvas",
size: "viewport",
})
.then(function (response) {
$(".crop_image").html("Image Upload");
$(".crop_image").attr("disabled", false);
$("#service_image").val(response);
$("#show_cropped_image_service").html('<img src="' + response + '">');
$("#uploadserviceimageModal_edit").modal("hide");
$(".modal-backdrop"). remove();
$("#exampleModal-1").modal("show");
});
});
});
