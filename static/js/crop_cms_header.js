
$(document).ready(function () {
$img_crop = $("#cms_image_edit").croppie({
enableExif: false,
viewport: {
width: 1366,
height: 767,
type: "square",
},
boundary: {
width:1366,
height: 767,
},
enableOrientation: false,
});
$("#id_cms_Image").on("change", function () {
var status = true;
var read = new FileReader();
var fi = document.getElementById('id_cms_Image');
if (fi.files.length > 0) {
for (var i = 0; i <= fi.files.length - 1; i++) {

var fsize = fi.files.item(i).size;
console.log(fsize)
var file = Math.round((fsize / 2024));

if (file > 2024) {

alert("Image is too Big, please select a image less than 2MB size.");
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
if (height >= 767 && width >= 1366) {
$img_crop
.croppie("bind", {
url: event.target.result,
})
.then(function () {
console.log("jQuery bind complete");
});
$("#uploadimageModal_edit").modal("show");

} else {
status = false;
alert("Please select image greater than 1366*767 px.");
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
$("#show_cropped_image").html('<img src="' + response + '" style="height: 249px;width: 768px;">');
$("#uploadimageModal_edit").modal("hide");

});
});
});
