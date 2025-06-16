document.addEventListener('DOMContentLoaded', function() {
    // 获取配置下拉菜单元素
    const configSelect = document.getElementById('configSelect');

    // 监听配置下拉菜单的点击事件
    configSelect.addEventListener('focus', loadConfigFiles);

    // 监听配置下拉菜单的展开事件（兼容不同浏览器）
    configSelect.addEventListener('click', function() {
        if (this.size === 1) {
            loadConfigFiles();
        }
    });

    // 加载配置文件列表
    function loadConfigFiles() {
        // 获取配置文件列表
        fetch('/api/config/files')
            .then(response => response.json())
            .then(data => {
                console.log('获取配置文件列表请求信息:', data);
                if (data.code === 200) {
                    console.log('获取配置文件列表成功:', data);
                    // 清空现有选项（保留第一个提示选项）
                    const firstOption = configSelect.options[0];
                    configSelect.innerHTML = '';
                    configSelect.appendChild(firstOption);

                    // 从请求结果中获取文件名
                    const files = extractFilesNames(data);
                    if (Array.isArray(files)) {
                    // 添加从服务器获取的最新配置文件
                    files.forEach(file => {
                        const option = document.createElement('option');
                        option.value = file;
                        option.textContent = file;
                        configSelect.appendChild(option);
                    });
                } else {
                    console.error('获取的配置文件数据不是数组:', files);
                }

                } else {
                    console.error('获取配置文件列表失败:', data);
                    // alert('获取配置文件列表失败，请稍后再试。');
                }
            })
            .catch(error => {
                console.error('获取文件列表错误:', error);
                // alert('获取文件列表错误，请稍后再试。', error);
            });
    }

    // 从API响应中提取书签组名称
    function extractFilesNames(data) {
        const files = [];
        data.files.forEach(file => {
            console.log('001-获取配置文件详情:', file);
            files.push(file);
        });
        // 打印配置文件列表
        console.log('获取配置文件列表成功:', files);
        return files;
    }

    // 加载配置文件列表—— 等待版本
    async function loadConfigFiles_waiting() {
        try {
            const response = await fetch('/api/config/files');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();

            if (data.status === 'success') {
                // 清空现有选项（保留第一个提示选项）
                const firstOption = configSelect.options[0];
                configSelect.innerHTML = '';
                configSelect.appendChild(firstOption);

                // 添加从服务器获取的最新配置文件
                data.data.forEach(config => {
                    const option = document.createElement('option');
                    option.value = config.name;
                    option.textContent = config.name;
                    configSelect.appendChild(option);
                });
            } else {
                console.error('获取配置文件列表失败:', data.detail);
            }
        } catch (error) {
            console.error('加载配置文件时出错:', error);
        }
    }

    // 页面加载时初始化加载配置文件列表
    // loadConfigFiles();
});