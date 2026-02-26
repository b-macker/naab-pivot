#!/usr/bin/env node
// Test fixture: JavaScript compute-intensive code

function heavyComputation(n) {
    // Nested loops - should recommend Go or C++
    let result = 0;
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < 100; j++) {
            result += Math.sqrt(i * j + 1);
        }
    }
    return result;
}

function mathOperations(x) {
    // Math-heavy - should recommend C++
    let val = x;
    for (let i = 0; i < 1000; i++) {
        val = Math.sqrt(val + 0.01);
        val *= 1.0001;
    }
    return val;
}

function arrayProcessing(arr) {
    // Array manipulation - medium complexity
    return arr
        .map(x => x * 2)
        .filter(x => x > 10)
        .reduce((sum, x) => sum + x, 0);
}

if (require.main === module) {
    const args = process.argv.slice(2);
    if (args.length === 0) {
        console.log("READY");
    } else {
        const input = parseInt(args[0]);
        const result = heavyComputation(input);
        console.log(result.toFixed(15));
    }
}

module.exports = { heavyComputation, mathOperations, arrayProcessing };
