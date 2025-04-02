import React from "react";
import Button from "../components/Button";
import CoinTable from "../components/CoinTable";
import "./MainPage.css"


const MainPage: React.FC = () => {
    return (
        <div className="page-container bg-gray-200">
            <p className="font-sans font-bold text-slate-900 text-xl tracking-wide">My coins</p>
            <div className="page-table">
                <CoinTable/>
            </div>
            <div className="page-buttons">
                <Button label="Add Coin" onClick={() => {}} />
                <Button label="Update Coin" onClick={() => {}} variant="update" />
                <Button label="Delete Coin" onClick={() => {}} variant="delete" />
            </div>
        </div>
    );
};

export default MainPage;
