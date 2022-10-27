
import "./Header.css"

function Header(props) {
    return (<><div className="Header">
                {props.name1}
                </div>
                <div className="Header2">
                {props.name2}
                </div>
            </>
    )
}

export default Header;
