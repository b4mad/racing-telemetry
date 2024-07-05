    const relayoutCallback = function(eventdata) {
        if (eventdata['xaxis.range[0]'] && eventdata['xaxis.range[1]']) {
            graphDivs.forEach(graphDiv => {
                if (graphDiv === timeGraphDiv) {
                    return;
                }
                Plotly.relayout(graphDiv, {
                    'xaxis.range[0]': eventdata['xaxis.range[0]'],
                    'xaxis.range[1]': eventdata['xaxis.range[1]']
                });
            });

            const trace = speedGraphDiv.data[graphIndex];
            const minDistance = parseFloat(eventdata['xaxis.range[0]']);
            const maxDistance = parseFloat(eventdata['xaxis.range[1]']);
            // find the first point where the distance is greater than the minDistance
            const maxIndex = trace.x.findIndex(x => x > maxDistance);
            const minIndex = trace.x.findIndex(x => x > minDistance);

            const mapTrace = mapDiv.data[0];
            // in mapTrace, iterate from minIndex to maxIndex and find the smallest and largest x and y values
            let smallestX = mapTrace.x[minIndex];
            let largestX = mapTrace.x[minIndex];
            let smallestY = mapTrace.y[minIndex];
            let largestY = mapTrace.y[minIndex];

            for (let i = minIndex; i <= maxIndex; i++) {
                const x = mapTrace.x[i];
                const y = mapTrace.y[i];
                if (x < smallestX) {
                    smallestX = x;
                }
                if (x > largestX) {
                    largestX = x;
                }
                if (y < smallestY) {
                    smallestY = y;
                }
                if (y > largestY) {
                    largestY = y;
                }
            }

            const margin = 50;
            Plotly.relayout(mapDiv, {
                'xaxis.range[0]': smallestX - margin,
                'xaxis.range[1]': largestX + margin,
                'yaxis.range[0]': smallestY - margin,
                'yaxis.range[1]': largestY + margin,
            });
        }
    }