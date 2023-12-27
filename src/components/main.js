import React from "react";
import "./main.css";

export default class MainArea extends React.Component {
  render() {
    return (
      <div className="main-area">
        {/* Animation Background */}
        <div className="background__animation">
          <div className="bg-circles">
            <div className="circle-1">
              <img
                src={process.env.PUBLIC_URL + "/images/gmail.png"}
                alt="gmail logo"
              />
            </div>
            <div className="circle-2"></div>
            <div className="circle-3">
              <img
                src={process.env.PUBLIC_URL + "/images/gpt_logo.png"}
                alt="gpt logo"
              />
            </div>
            <div className="circle-4">
              <img
                src={process.env.PUBLIC_URL + "/images/gpt_logo.png"}
                alt="gpt logo"
              />
            </div>
            <div className="effect-1">
              <img
                src={process.env.PUBLIC_URL + "/images/gmail.png"}
                alt="gmail logo"
              />
            </div>
          </div>
        </div>
        {/* Main Content */}
        <div className="tagline important gradient-text">
          AI Powered Mail.
          <br />
          AI Powered Future.
        </div>
        <div className="below-tagline">
          Use Bonsai's AI technology to send short summaries of your important
          emails straight to your phone.
        </div>
        {/* make a scrolling down button arrow animation here  */}
        <div className="button-container">
          <div className="button">
            <div class="scroll-down2"></div>
          </div>
        </div>
        <div className="main-body">
          <div className="image-cell">
            <img src="images/computer-phone.svg" className="cell-image"></img>
          </div>
          <div className="text-cell">
            <div className="title important gradient-text">
              Increase Productivity
            </div>
            Sync your email with your phone for snappy, easy-to-digest alerts
            that keep you in the loop, effortlessly!
          </div>
          <div className="text-cell reversed">
            <div className="title important reversed gradient-text">
              Expand Your Network
            </div>
            Auto-translate emails into your native tongue, effortlessly breaking
            language barriers and expanding your global connections!
          </div>
          <div className="image-cell">
            <img src="images/tree.svg" className="cell-image"></img>
          </div>
          <div className="image-cell">
            <img src="images/analytics.svg" className="cell-image"></img>
          </div>
          <div className="text-cell">
            <div className="title important gradient-text">
              AI-Powered Analytics
            </div>
            Unlock email insights with Bonsai's analytics, supercharged by
            cutting-edge language models!
          </div>

          <br />
          <br />
        </div>
        <div className="bottom-section">
          <p>
            Bonsai isn't available to the public yet, but you can join our
            waitlist to have the first chance to sign up as soon as we go live.
          </p>
          <div className="header-element sign-up-b">Join our Waitlist</div>
        </div>
        {/* Footer  */}
        <div className="footer">
          <div className="footer-text">
            <div className="footer-title">Bonsai</div>
            <div className="footer-subtitle">AI Powered Mail</div>
            <div className="footer-subtitle">AI Powered Future</div>
          </div>
        </div>
      </div>
    );
  }
}
