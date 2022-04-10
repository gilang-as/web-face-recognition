import Webcam from "react-webcam";
import React, {useEffect, useRef, useState} from 'react';
import axios from "axios";

function useCanvas(){
    const canvasRef = useRef(null);
    const [coordinates, setCoordinates] = useState({faces: [], names: []});

    useEffect(()=>{
        const canvasObj = canvasRef.current;
        const ctx = canvasObj.getContext('2d');
        canvasObj.width = 1280;
        canvasObj.height = 720;
        ctx.clearRect( 0,0, 1280, 720 );
        coordinates.faces.forEach((coordinate, index)=>{draw(ctx, coordinate, coordinates.names[index])});
    });

    return [ coordinates, setCoordinates, canvasRef ];
}

function draw(ctx, face, name){
    let xLength =  face[1] - face[3]
    let yLength = face[2] - face[0]
    ctx.font = 'bold 20px Courier';
    ctx.shadowColor = 'transparent';
    ctx.fillStyle = 'red';
    ctx.strokeStyle = "red";
    ctx.lineWidth = "2";
    //(y0,x1,y1,x0)
    ctx.fillText(name, face[3],  face[2] + 18);
    ctx.rect(face[3], face[0], xLength, yLength);
    ctx.stroke();

    // .restore(): Canvas 2D API restores the most recently saved canvas state
    ctx.restore();
}

const App = () => {

    const [coordinates, setCoordinates, canvasRef] = useCanvas();
    const webcamRef = useRef(null);
    useEffect(() => {

        const interval = setInterval(async () => {
            const image = webcamRef.current.getScreenshot({width: 1280, height: 720});
            if (image !=="" || image !== null){
                const res = await axios.post("http://localhost:8081/v1/face-recognize", {
                    im_b64: image.split(",")[1]
                });
                setCoordinates({faces: res?.data?.faces, names: res?.data?.names});
            }
        }, 1000);
        return () => clearInterval(interval);
    }, [coordinates, setCoordinates]);

    return (
        <main className="App-main" >
            <div style={{position: "relative"}}>
                <Webcam
                    ref={webcamRef}
                    mirrored
                    style={{
                        width: "50%", height: "25%"
                    }}
                    videoConstraints={{width: 1280, height: 720, facingMode: "user"}}
                />
                <canvas
                    className="App-canvas"
                    ref={canvasRef}
                    style={{
                        width: "50%", position: "absolute", top: "0", left: "0"
                    }} />
            </div>
        </main>
    );
}
export default App;