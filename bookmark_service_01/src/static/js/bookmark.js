document.addEventListener('DOMContentLoaded', function() {
    // 获取下拉菜单元素
    const groupSelect = document.getElementById('group_name');
    
    // 监听下拉菜单的点击事件
    groupSelect.addEventListener('focus', fetchGroups);
    
    // 监听下拉菜单的展开事件（兼容不同浏览器）
    groupSelect.addEventListener('click', function() {
        if (this.size === 1) {
            fetchGroups();
        }
    });
    
    // 从服务器获取最新的书签组数据
    function fetchGroups() {
        fetch('/api/bookmarks')
            .then(response => response.json())
            .then(data => {
                // 清空现有选项（保留第一个提示选项）
                const firstOption = groupSelect.options[0];
                groupSelect.innerHTML = '';
                groupSelect.appendChild(firstOption);
                
                // 添加从服务器获取的最新书签组
                const groups = extractGroupNames(data);
                groups.forEach(group => {
                    const option = document.createElement('option');
                    option.value = group;
                    option.textContent = group;
                    groupSelect.appendChild(option);
                });
            })
            .catch(error => {
                console.error('获取标签组错误:', error);
                alert('加载标签组错误，请稍后再试。', error);
            });
    }
    
    // 从API响应中提取书签组名称
    function extractGroupNames(data) {
        const groups = [];
        data.forEach(group => {
            const groupName = Object.keys(group)[0];
            groups.push(groupName);
        });
        return groups;
    }
    
    // 处理表单提交
    document.getElementById('addBookmarkForm').addEventListener('submit', function (e) {
        e.preventDefault();
        const groupName = document.getElementById('group_name').value || document.getElementById('new_group_name').value;
        const serviceName = document.getElementById('service_name').value;
        const abbr = document.getElementById('abbr').value;
        const url = document.getElementById('url').value;
        
        if (!groupName) {
            alert('Please select or enter a group name');
            return;
        }
        
        const data = {
            group_name: groupName,
            service_name: serviceName,
            abbr: abbr,
            url: url
        };
        
        fetch('/api/bookmarks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            alert(result.message);
            if (result.code === 200) {
                // 重新加载窗口
                // window.location.reload();
            }
        });
    });
});
