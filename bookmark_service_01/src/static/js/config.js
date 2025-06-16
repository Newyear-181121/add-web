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
    async function loadConfigFiles() {
        try {
            const response = await fetch('/api/config/files');
            const data = await response.json();

            if (data.status === 'success') {
                // 清空现有选项
                configSelect.innerHTML = '<option value="">请选择配置文件...</option>';

                // 添加配置文件选项
                data.data.forEach(config => {
                    const option = document.createElement('option');
                    option.value = config.name;
                    option.textContent = config.name;
                    configSelect.appendChild(option);
                });
            }
        } catch (error) {
            console.error('错误的加载配置文件:', error);
        }
    }
});
