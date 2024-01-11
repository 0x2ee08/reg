var video = document.getElementById('video');
var i = 0

var url_link = location.protocol+"//"+location.hostname+"/api/"

if (location.protocol !== 'https:') {
  location.replace(`https:${location.href.substring(location.protocol.length)}`);
}

navigator.mediaDevices.getUserMedia({ video: true }).then(function (stream) {
  video.srcObject = stream;
  video.play();
});

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}


function takePhotos(i) {
  var canvas = document.getElementById('canvas');
  var context = canvas.getContext('2d');

  context.drawImage(video, 0, 0, 640, 480);

  let image_data_url = canvas.toDataURL('image/jpeg');

  var img = document.createElement('img');

  img.src = image_data_url;
  img.style.height = "142px";
  img.style.width = "190px";

  document.getElementById('photos').appendChild(img);

  return [String(i + 1), image_data_url]
};

function snap(info) {
  if (i == 0) {
    alert("Hãy bỏ khẩu trang")
    val = takePhotos(i)
    info['uri' + i] = val[1]
    i = parseInt(val[0])
  }
  else if (i == 100) {
    alert("Hãy đeo khẩu trang")
    val = takePhotos(i)
    info['uri' + i] = val[1]
    i = parseInt(val[0])
  }
  else if (i > 200) {
    const options = {
      method: 'POST',
      body: JSON.stringify(info)
    };
    alert("Đang tải dữ liệu lên server, đợi chút nhé. Không đóng hoặc reload lại trang !!!")
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
    fetch(url_link + 'upload_image_uri', options).then(res => res.text()).then(data => {
      if (data == "success") {
        alert("Đã hoàn thành đăng kí")
        location.reload()
      }
      else {
        alert("Đã xảy ra lỗi, vui lòng đăng kí lại")
        location.reload()
      }
    });
  }
  else {
    val = takePhotos(i)
    info['uri' + i] = val[1]
    i = parseInt(val[0])
  }
}


document.getElementById('snap').addEventListener('click', function (event) {
  let uid = document.getElementById('uid').value;

  let flag = 1;

  const info = {
    "uid": uid
  }
  const options = {
    method: 'POST',
    body: JSON.stringify(info)
  };

  //change URL here:
  fetch(url_link + 'check_uid', options).then(res => res.text()).then(data => {
    if (data == "false") {
      alert("Sai mã học sinh/ giáo viên");
      flag = 0;
      location.reload();
    }
  });

  const info2 = {
    "uid": uid
  }

  setTimeout(async function () {
    await sleep(1000)
    if (flag == 1) {
      for (let i = 0; i < 202; i++) {
        snap(info2)
        await sleep(100)
      }
    }
  }, 500);
});