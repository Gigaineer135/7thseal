#!/usr/bin/bash
'''
Dev: Surgat

                                                     @#@@@@@@@#@
                                                &@@,@           @,@@&
                                             @@.                     ,@@
                                           @&                           @@
                                         %@
                                        &@
                                        @
                                       &@
                @@@@@@                 &@
            .@@*      @@&              &@
          *@             @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
         /@                            &@
         &@                            &@
         .@                            &@
           @&           .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
             #@@%,   @@@               &@
                  @@@@                 &@
                                       &@
                                       &@                                     %@@
                                       &@                  @@                    @*
                                       &@                 @. @*                  #@
                                       &@               ,@.   @#                .@,
                                       &@@@@@@@@@@@@@@@/@@@@@@@@&@@@@@@@@@@@@@@@@#
                                                      #@        @@
                                                     @@          &@
                                                    @@            (@
                                                    @%@@@@@@@@@@@@@@@
'''
apt install gpsd
apt install gpsd-clients
apt install python3-pip
pip3 install tk
rm -rf /etc/7thseal
gpsd -D 5 -N -n /dev/ttyUSB0
mv 7thseal.py /sbin/7thsealconf.py
echo '#!/usr/bin/bash' > /sbin/7thseal
echo "python3  /sbin/7thsealconf.py" >> /sbin/7thseal
chmod 777 /sbin/7thsealconf.py /sbin/7thseal
chattr +i  /sbin/7thsealconf.py
