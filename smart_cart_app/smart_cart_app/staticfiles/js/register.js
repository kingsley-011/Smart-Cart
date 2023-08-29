const video = document.getElementById("webcam-video");
const canvas = document.getElementById("canvas");
const captureButton = document.getElementById("capture-button");
const form = document.getElementById("registration-form");

// Access the user's webcam
async function initWebcam() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
  } catch (error) {
    console.error("Error accessing webcam:", error);
  }
}

// Capture an image from the webcam and convert it to a base64 data URL
function captureImage() {
  const context = canvas.getContext("2d");
  context.drawImage(video, 0, 0, canvas.width, canvas.height);

  // Get the base64 data URL of the captured image
  const imageDataURL = canvas.toDataURL("image/jpeg");

  // Display the base64 data URL in a hidden input field
  const hiddenImageInput = document.createElement("input");
  hiddenImageInput.type = "hidden";
  hiddenImageInput.name = "webcamImage";
  hiddenImageInput.value = imageDataURL;
  form.appendChild(hiddenImageInput);

  console.log("Image captured:", imageDataURL);
}

// Initialize the webcam and set up the capture button
function setup() {
  initWebcam();
  captureButton.addEventListener("click", captureImage);
}

setup();
