function sendMovieID(movieID) {
    // 检查用户是否已登录
    if ("{{ user }}" !== "None") {
        // 构建带参数的 URL
        const url = `/save_history?movieID=${movieID}`;

        fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => console.error('Error:', error));
        console.log("sendMovieID function is called.");
    } else {
        console.log("用户未登录，不能记录点击记录。");
    }
}


function showInfo(element) {
    // 在这里编写显示信息的代码
    // 例如，显示元素的信息
    element.style.display = 'block';
    console.log("showInfo function is called.");
}

function hideInfo(element) {
    // 在这里编写隐藏信息的代码
    // 例如，隐藏元素的信息
    element.style.display = 'none';
    console.log("hideInfo function is called.");
}
