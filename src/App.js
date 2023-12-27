import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Menubar from "./components/menubar";
import Main from "./components/main";
import Settings from "./components/Settings";

function App() {
  return (
    <>
      <Router>
        <Routes>
          <Route
            path="/"
            element={
              <>
                <Menubar />
                <Main />
              </>
            }
          />
          <Route
            path="/profile"
            element={
              <>
                <Menubar />
                <Settings />
              </>
            }
          />
        </Routes>
      </Router>
    </>
  );
}

export default App;
