var navOpen = false;
var x = document.getElementsByClassName('side-item');
function openNav() {
    if (navOpen)
    {
      document.getElementById("navbar").style.left = "0px";
      document.getElementById("sidebar").style.left = "-250px";
      document.getElementById("nav-button-i").className = "open-sidenav-btn fa fa-bars";
      navOpen = false;
    }
    else
    {
      document.getElementById("sidebar").style.left = "0";
      document.getElementById("navbar").style.left = "250px";
      document.getElementById("nav-button-i").className = "open-sidenav-btn fa fa-chevron-left";
      navOpen = true;
    }
}
