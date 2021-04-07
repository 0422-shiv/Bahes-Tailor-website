
$(document).ready(function () {
$img_crop = $("#profile_image_edit").croppie({
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
$("#id_Profile_Image").on("change", function () {
var status = true;
var read = new FileReader();
var fi = document.getElementById('id_Profile_Image');
if (fi.files.length > 0) {
for (var i = 0; i <= fi.files.length - 1; i++) {

var fsize = fi.files.item(i).size;
 console.log(fsize)
var file = Math.round((fsize / 1024));
console.log(file);
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
if (height >= 289 && width >= 289) {
$img_crop
.croppie("bind", {
url: event.target.result,
})
.then(function () {
console.log("jQuery bind complete");
});


$("#uploadimageModal_edit").modal("show");
$("#exampleModal-7").modal("hide");
} else {
status = false;
alert("Please select image greater that 289*289px.");
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
$("#profile_image").val(response);
$("#show_cropped_image").html('<img src="' + response + '">');

$("#uploadimageModal_edit").modal("hide");
$("#exampleModal-7").modal("show");

});
});
});
