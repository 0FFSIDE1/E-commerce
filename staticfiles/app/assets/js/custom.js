// Function to get CSRF token from cookie or meta tag
function getCSRFToken() {
    // Try to get CSRF token from meta tag (this assumes you've included it in the HTML head)
    var csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    return csrfToken;
  }

// Function to Register a Vendor
document.addEventListener("DOMContentLoaded", () => {
    const RegisterVendorForm = document.getElementById("RegisterVendorForm");
    var toastEl = document.getElementById('cart-toast');
    var toastBody = toastEl.querySelector('.toast-body');
  
    RegisterVendorForm.addEventListener("submit", (event) => {
      event.preventDefault(); // Prevent the default form submission
  
      const formData = new FormData(RegisterVendorForm);
      const data = Object.fromEntries(formData.entries());
    //   data.create_account = formData.get("create_account") === "on"; // Convert checkbox value to boolean
  
      $.ajax({
        url: `/auth/dashboard/vendor/register`,
        type: 'POST',
        headers: {
          'X-CSRFToken': getCSRFToken(), // Include CSRF token in the headers
          'Content-Type': 'application/json'
        },
        data: JSON.stringify(data),
        success: function(response) {
          if (response.success) {
            console.log(response)
            
            checkoutBtn = document.getElementById('checkoutBtn')
            checkoutBtn.style.display = 'block'
           
            toastEl.className='bg-success'
            
            toastBody.innerText = response.message;
            var toast = new bootstrap.Toast(toastEl);
            toast.show();
          } else {
           
            
            toastEl.className='bg-danger'
           
            toastBody.innerText = response.message;
            var toast = new bootstrap.Toast(toastEl);
            toast.show();
          }
        },
        error: function(xhr, status, error) {
          console.error("Error:", error);
         
            toastEl.className='bg-danger'
            
            toastBody.innerText = error
            var toast = new bootstrap.Toast(toastEl);
            toast.show();
        }
      });
    });
  });





  // Function to Login a Vendor
document.addEventListener("DOMContentLoaded", () => {
  const LoginVendorForm = document.getElementById("LoginVendorForm");
  var toastEl = document.getElementById('cart-toast');
  var toastBody = toastEl.querySelector('.toast-body');

  LoginVendorForm.addEventListener("submit", (event) => {
    event.preventDefault(); // Prevent the default form submission

    const formData = new FormData(LoginVendorForm);
    const data = Object.fromEntries(formData.entries());


    $.ajax({
      url: `/auth/dashboard/vendor/login`,
      type: 'POST',
      headers: {
        'X-CSRFToken': getCSRFToken(), // Include CSRF token in the headers
        'Content-Type': 'application/json'
      },
      data: JSON.stringify(data),
      success: function(response) {
        if (response.success) {
          console.log(response)
          
          checkoutBtn = document.getElementById('checkoutBtn')
          checkoutBtn.style.display = 'block'
         
          toastEl.className='bg-success'
          
          toastBody.innerText = response.message;
          var toast = new bootstrap.Toast(toastEl);
          toast.show();
        } else {
         
          
          toastEl.className='bg-danger'
         
          toastBody.innerText = response.message;
          var toast = new bootstrap.Toast(toastEl);
          toast.show();
        }
      },
      error: function(xhr, status, error) {
        console.error("Error:", error);
       
          toastEl.className='bg-danger'
          
          toastBody.innerText = error
          var toast = new bootstrap.Toast(toastEl);
          toast.show();
      }
    });
  });
});