// LetterBlock.scad - Basic usage of text() and linear_extrude()

//vartest
vartest = "A";
LetterBlock(vartest);
vartest2 = 30;
vartest3=30;
sphere=true;
// A3D-Start
// Boolean [sphere]<First Checkbox>{This does a really cool thing!}
// Integer [vartest2]<An integer>{Enter an integer in mm}
// Integer [vartest3]<An integer>{Enter an integer in mm!!!}
// Integer [vartest4]<test>{Enter an integer in mm!!!!!!!!}
// Boolean [booleans!]<2nd Checkbox>{Hello world}
// A3D-End

// Module definition.
// size=30 defines an optional parameter with a default value.
module LetterBlock(letter, size=30) {
    difference() {
        translate([0,0,size/4]) cube([vartest3,vartest2,size/2], center=true);
        translate([0,0,size/6]) {
            // convexity is needed for correct preview
            // since characters can be highly concave
            linear_extrude(height=size, convexity=4)
                text(letter, 
                     size=size*22/30,
                     font="Bitstream Vera Sans",
                     halign="center",
                     valign="center");
        }
    }
    if (sphere) {
        sphere(15,15);
    }
    
}

echo(version=version());
// Written by Marius Kintel <marius@kintel.net>
//
// To the extent possible under law, the author(s) have dedicated all
// copyright and related and neighboring rights to this software to the
// public domain worldwide. This software is distributed without any
// warranty.
//
// You should have received a copy of the CC0 Public Domain
// Dedication along with this software.
// If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
