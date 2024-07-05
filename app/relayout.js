                // draw a circle at the x, y position of the closest point
                trace = mapDiv.data[0];
                const circleSize = 20;
                const circle = {
                    type: 'circle',
                    xref: 'x',
                    yref: 'y',
                    x0: trace.x[point.pointIndex] - circleSize,
                    y0: trace.y[point.pointIndex] - circleSize,
                    x1: trace.x[point.pointIndex] + circleSize,
                    y1: trace.y[point.pointIndex] + circleSize,
                    line: { color: 'red' }
                };

                // add an arrow to the circle, pointing in the direction of the yaw
                // Convert degrees to radians
                function degreesToRadians(degrees) {
                    return degrees * (Math.PI / 180);
                }

                const arrowLength = 100;
                const arrow = {
                    type: 'line',
                    x0: trace.x[point.pointIndex],
                    y0: trace.y[point.pointIndex],
                    x1: trace.x[point.pointIndex] + Math.cos(degreesToRadians(trace.yaw[point.pointIndex])) * arrowLength,
                    y1: trace.y[point.pointIndex] + Math.sin(degreesToRadians(trace.yaw[point.pointIndex])) * arrowLength,
                    line: { color: 'green' }
                };
                // console.log(trace.yaw[point.pointIndex]);

                Plotly.relayout(mapDiv, {
                    shapes: [
                        circle,
                        arrow
                    ]
                });
