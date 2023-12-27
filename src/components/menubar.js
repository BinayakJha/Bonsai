import React from "react";
import "./menubar.css";

export default class Menubar extends React.Component {
  render() {
    return (
      <div className="main">
        <a href="/"><img src="bonsai.svg" className="logo"/></a>
        <div className="header-element">About</div>
        <div className="header-element">For Buisness</div>
        <div className="header-element">Plans and Pricing</div>
        <div className="header-element">Support</div>
        <div className="divider"></div>
        <div className="header-element login">
          <a href="/login">Log in</a>
        </div>
        <div className="header-element sign-up">Join our Waitlist</div>
      </div>
    );
  }
}
