// index.js
document.getElementById("generate").onclick = function () {
    const input = document.getElementById("input").value;
    if (!input) {
        return alert('请输入内容');
    }
    fetchData(input, (data) => {
        // 回调时执行以下代码
        document.getElementById('output').innerHTML += data;
    });
}

const fetchData = async function (input, callback) {
    const response = await fetch('/api/generate', {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt: input })
    })

    const reader = response.body.getReader();
    // 获取实时返回的数据
    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const data = new TextDecoder().decode(value);
        // 这是一个回调函数
        callback(data)
    }
};

document.getElementById('save-button').onclick = function () {
    const tip = document.getElementById('input').value;
    const content = document.getElementById('output').innerHTML;
    if (!tip || !content) {
        return alert('数据不能为空')
    }
    createWriting(tip, content)
}

// 创建数据，请求后台接口
const createWriting = async function (tip, content) {
    const response = await fetch('/api/create', {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ tip, content })
    })
    if (response.status === 200) {
        alert('数据添加成功')
        window.location.reload()
    }
}

// 删除数据，请求后台接口
const hanldeDelete = async function (id) {
    const response = await fetch(`/api/delete/${id}`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
        }
    })
    if (response.ok) {
        window.location.reload()
    }
}