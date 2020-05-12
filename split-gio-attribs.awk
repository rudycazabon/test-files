#!/usr/bin/awk -f

BEGIN { print "START" }
/standard::name:/ { RS=""; print $1 $2 }
/metadata::nautilus-icon-position:/ { 
    split($2,a,","); 
    print $1 "x=" a[1], "y=" a[2] "\t" 
}
/metadata::icon-scale:/ { print $1 }
END { print "DONE" }