####################
# PLF build
%define build_plf 0
####################

%define enable_extrusion 1
%define disable_inappropriate 1
# Allow --with[out] <feature> at rpm command line build
%{?_with_plf: %{expand: %%global build_plf 1}}
%{?_without_plf: %{expand: %%global build_plf 0}}
%{?_with_extrusion: %{expand: %%global enable_extrusion 1}}
%{?_without_extrusion: %{expand: %%global enable_extrusion 0}}
%{?_with_inappropriate: %{expand: %%global disable_inappropriate 0}}
%{?_without_inappropriate: %{expand: %%global disable_inappropriate 1}}

%if %{build_plf}
%define distsuffix plf
%if %{mdvver} >= 201100
# make EVR of plf build higher than regular to allow update, needed with rpm5 mkrel
%define extrarelsuffix plf
%endif
%endif

Summary:	A set of X Window System screensavers
Name:		xscreensaver
Version:	5.22
Release:	2%{?extrarelsuffix}
License:	BSD
Group:		Graphical desktop/Other
URL:		http://www.jwz.org/xscreensaver/
Source0:	http://www.jwz.org/xscreensaver/%{name}-%{version}.tar.gz
Source1:	xscreensaver-capplet.png
Source2:	dmctl
Patch0:		xscreensaver-5.05-mdv-alt-drop_setgid.patch
# Don't check login manager in PATH because we use custom wrapper
Patch1:		xscreensaver-5.15-lmcheck.patch
# Only GDadou should be enabled
Patch9:		xscreensaver-5.15-defaultconfig.patch
# (fc) 4.00-4mdk allow root to start xscreensaver
Patch10:	xscreensaver-4.23-root.patch
# (fc) 4.05-3mdk disable openGL hacks by default
Patch11:	xscreensaver-5.09-noGL.patch
# (fc) 4.23-1mdk disable inappropriate stuff (Mdk bug #19866)
Patch19:	xscreensaver-5.00-inappropriate.patch
Requires:	xscreensaver-common = %{version}-%{release}
#Requires:	fortune-mod
Requires:	mandriva-theme-screensaver
Requires:	xdg-utils
BuildRequires:	makedepend
BuildRequires:	bc
#BuildRequires:	fortune-mod
BuildRequires:	jpeg-devel
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(gdk-pixbuf-xlib-2.0)
BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(xpm)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(xxf86misc)
BuildRequires:	pkgconfig(xxf86vm)
%if %{enable_extrusion}
BuildRequires:	gle-devel
%endif
BuildRequires:	imagemagick

%description
The xscreensaver package contains a variety of screensavers for your
mind-numbing, ambition-eroding, time-wasting, hypnotized viewing
pleasure.

Install the xscreensaver package if you need screensavers for use with
the X Window System.

%if %{build_plf}
This package is in restricted as it contains copyrighted images.
%endif

%package base
Summary:	A set of screensavers
Group:		Graphical desktop/Other
Requires:	xscreensaver-common = %{version}-%{release}
Conflicts:	xscreensaver < 5.00-2
Requires:	words

%description base
Various screensavers used by Xscreensaver.

%package common
Summary:	Utilities used by xscreensaver screensavers
Group:		Graphical desktop/Other
Conflicts:	xscreensaver < 5.00-2
Provides:	xscreensaver-utils
Requires:	chbg

%description common
Utilities used by xscreensaver screensavers.

%package gl
Summary:	A set of GL screensavers
Group:		Graphical desktop/Other
Requires:	xscreensaver-common = %{version}-%{release}
Requires(post):	xscreensaver-common = %{version}-%{release}
Requires(postun):	xscreensaver-common = %{version}-%{release}

%description gl
The xscreensaver-gl package contains even more screensavers for your
mind-numbing, ambition-eroding, time-wasting, hypnotized viewing
pleasure. These screensavers require OpenGL or Mesa support.

Install the xscreensaver-gl package if you need more screensavers for
use with the X Window System and you have OpenGL or Mesa installed.

%if %{build_plf}
%package matrix
Summary:	The Matrix screensavers
Group:		Graphical desktop/Other
Requires:	xscreensaver-common = %{version}-%{release}

%description matrix
The xscreensaver-matrix package contains two screensavers for
xscreensaver based on the movie The Matrix. It is in restricted because
there might by copyright problems with the artwork used in this
screensavers.
%endif

%if %{enable_extrusion}
%package extrusion
Summary:	OpenGL screensaver
Group:		Graphical desktop/Other
Requires:	xscreensaver-common = %{version}-%{release}

%description extrusion
The xscreensaver-extrusion package contains the extrusion
screensaversfor your mind-numbing, ambition-eroding, time-wasting,
hypnotized viewing pleasure. This screensaver requires OpenGL or Mesa
support.

This screensaver is in a separate package, because it is the only
application for the Mandriva Linux distribution which requires the GLE
extrusion library.
%endif

%prep
%setup -q
%patch1 -p1 -b .login-manager
# WARNING this patch must ALWAYS be applied, if it fails, REGENERATE it !!!
%patch9 -p1 -b .defaultconfig
%patch10 -p1 -b .root
%patch11 -p1 -b .noGL
%if %{disable_inappropriate}
%patch19 -p1 -b .inappropriate
%endif

# Needed by patches 1 and 11
autoconf

%build
%configure2_5x \
    --enable-locking \
    --enable-root-passwd \
    --with-browser=xdg-open \
    --with-dpms-ext \
    --with-xinerama-ext \
    --with-xf86vmode-ext \
    --with-xf86gamma-ext \
    --with-randr-ext \
    --with-proc-interrupts \
    --with-login-manager=dmctl \
    --without-shadow \
    --with-pixbuf \
    --with-xpm \
    --with-jpeg \
    --with-xshm-ext \
    --with-xdbe-ext \
    --without-readdisplay \
    --without-setuid-hacks \
    --with-gtk \
    --without-motif \
    --with-pam \
    --with-gl \
    --with-image-directory="%{_datadir}/mdk/screensaver" \
    --without-kerberos \
%if %{enable_extrusion}
    --with-gle
%else
    --without-gle
%endif

make depend
%make

%install
rm -rf %{buildroot} gl-extras.files base.files %{name}.lang
mkdir -p %{buildroot}%{_sysconfdir}/X11/app-defaults/
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man6
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
mkdir -p %{buildroot}%{_libexecdir}/xscreensaver

make install_prefix=%{buildroot} bindir=%{_bindir} \
 KDEDIR=%{_prefix} GNOME_BINDIR=%{_bindir}  GNOME_DATADIR=%{_datadir} \
 mandir=%{_mandir} AD_DIR=%{_sysconfdir}/X11/app-defaults/ \
 gnulocaledir=%{_datadir}/locale install

# Custom wrapper for gdmflexiserver and kdmctl
install -m 755 %{SOURCE2} %{buildroot}%{_bindir}/dmctl

cat<<EOF >README.GL
The xscreensaver-gl package contains even more screensavers for your
mind-numbing, ambition-eroding, time-wasting, hypnotized viewing
pleasure. These screensavers require OpenGL or Mesa support.

Install the xscreensaver-gl package if you need more screensavers for
use with the X Window System and you have OpenGL or Mesa installed.
EOF

#icons
mkdir -p %{buildroot}%{_datadir}/pixmaps
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
cp %{SOURCE1}  %{buildroot}%{_datadir}/pixmaps
convert -scale 16x16 %{SOURCE1} %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
convert -scale 32x32 %{SOURCE1} %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
ln -s %{_datadir}/pixmaps/xscreensaver-capplet.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

#remove unpackaged files
rm -f %{buildroot}%{_datadir}/xscreensaver/config/xjack.xml
rm -f %{buildroot}%{_mandir}/man6/xjack.6
rm -f  %{buildroot}%{_libexecdir}/xscreensaver/xjack

%if ! %{build_plf}
rm -rf %{buildroot}%{_libexecdir}/xscreensaver/*matrix
rm -rf %{buildroot}%{_mandir}/man6/*matrix*
rm -rf %{buildroot}%{_datadir}/xscreensaver/config/*matrix*
%endif
%if ! %{enable_extrusion}
rm -f %{buildroot}%{_datadir}/xscreensaver/config/extrusion.xml
rm -f %{buildroot}%{_mandir}/man6/extrusion.6
%endif

%find_lang %{name}

# This function prints a list of things that get installed.
# It does this by parsing the output of a dummy run of "make install".
#
list_files() {
  make -s install_prefix=%{buildroot} mandir=%{_mandir}/ \
  bindir=%{_bindir} INSTALL=true "$@"	\
   | sed -n -e 's@.* \(/[^ ]*\)$@\1@p'				\
   | sed    -e "s@^%{buildroot}@@"				\
	    -e "s@/[a-z][a-z]*/\.\./@/@"			\
   | sed    -e 's@\(.*/man/.*\)@\1\*@'				\
   | sed    -e 's@\(.*/app-defaults/\)@%config \1@'		\
	    -e 's@\(.*/pam\.d/\)@%config(missingok) \1@'	\
   | sort
}

# Generate three lists of files for the three packages.
#
dd=%{_builddir}/%{name}-%{version}
( cd hacks/glx ; list_files install > $dd/gl-extras.files)
( cd hacks     ; list_files install > $dd/base.files)

#gw remove the files we don't package:
perl -pi -e "s/.*(gdadou|xjack|matrix|extrusion).*//" gl-extras.files base.files

%find_lang %{name}

%post gl
sed -i -e 's/\A-\s+GL:/ GL:/' %{_sysconfdir}/X11/app-defaults/XScreenSaver

%postun gl
sed -i -e '/\A\s*GL:/ and print "- $_" or print "$_"' %{_sysconfdir}/X11/app-defaults/XScreenSaver

%files -f %{name}.lang
%config(noreplace) %{_sysconfdir}/pam.d/xscreensaver
%doc README
%{_mandir}/man1/xscreensaver-command.1*
%{_mandir}/man1/xscreensaver-demo.1*
%{_mandir}/man1/xscreensaver.1*
%attr(755,root,chkpwd) %{_bindir}/xscreensaver
%{_bindir}/xscreensaver-command
%{_bindir}/xscreensaver-demo
%{_bindir}/dmctl
%dir %{_datadir}/xscreensaver
%{_datadir}/xscreensaver/glade
%{_datadir}/applications/xscreensaver-properties.desktop
%{_datadir}/pixmaps/*
%{_datadir}/xscreensaver/config/gdadou.xml
%{_iconsdir}/hicolor/*/apps/*.png

%files common
%config(noreplace) %{_sysconfdir}/X11/app-defaults/*
%dir %{_libexecdir}/%{name}
%{_bindir}/xscreensaver-getimage
%{_bindir}/xscreensaver-getimage-file
%{_bindir}/xscreensaver-getimage-video
%{_bindir}/xscreensaver-text
%{_mandir}/man1/xscreensaver-getimage*
%{_mandir}/man1/xscreensaver-text.1*
%dir %{_datadir}/%{name}/config
%{_datadir}/%{name}/config/README

%files base -f base.files

%files gl -f gl-extras.files
%doc README.GL

%if %{enable_extrusion}
%files extrusion
%doc README.GL
%{_datadir}/xscreensaver/config/extrusion.xml
%{_mandir}/man6/extrusion.6*
%{_libexecdir}/xscreensaver/extrusion
%endif

%if %{build_plf}
%files matrix
%doc README.GL
%{_mandir}/man6/xmatrix.6*
%{_mandir}/man6/glmatrix.6*
%{_datadir}/xscreensaver/config/glmatrix.xml
%{_datadir}/xscreensaver/config/xmatrix.xml
%{_libexecdir}/xscreensaver/xmatrix
%{_libexecdir}/xscreensaver/glmatrix
%endif



%changelog
* Wed Apr 25 2012 Andrey Bondrov <abondrov@mandriva.org> 5.15-1mdv2012.0
+ Revision: 793381
- Update BuildRequires
- We don't need to modify desktop file anymore, it's already fixed upstream
- Adopt PLF build to new MDV/Rosa realities
- Use custom wrapper (dmctl) as login manager, update BuildRequires
- Rediff default config patch and minor spec cleanup

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - update to new version 5.15

* Tue May 24 2011 GÃ¶tz Waschk <waschk@mandriva.org> 5.14-1
+ Revision: 678080
- new version
- rediff patch 9
- drop obsolete configure options
- fix extrarelsuffix again

* Fri May 20 2011 GÃ¶tz Waschk <waschk@mandriva.org> 5.13-2
+ Revision: 676302
- readd missing extrarelsuffix for plf

* Thu May 19 2011 GÃ¶tz Waschk <waschk@mandriva.org> 5.13-1
+ Revision: 676139
- new version
- rediff patch 9

* Sun May 15 2011 Oden Eriksson <oeriksson@mandriva.com> 5.12-6
+ Revision: 674749
- rebuild

* Sun Feb 27 2011 Funda Wang <fwang@mandriva.org> 5.12-5
+ Revision: 640299
- rebuild to obsolete old packages

* Mon Feb 21 2011 GÃ¶tz Waschk <waschk@mandriva.org> 5.12-4
+ Revision: 639092
- rebuild

  + Anssi Hannula <anssi@mandriva.org>
    - plf: append "plf" to Release on cooker to make plf build have higher EVR
      again with the rpm5-style mkrel now in use

* Wed Feb 02 2011 Funda Wang <fwang@mandriva.org> 5.12-3
+ Revision: 635147
- rebuild
- tighten BR

* Wed Oct 06 2010 GÃ¶tz Waschk <waschk@mandriva.org> 5.12-2mdv2011.0
+ Revision: 583606
- work around rpm bug #61207

* Sun Oct 03 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 5.12-1mdv2011.0
+ Revision: 582752
- update to new version 5.12
- disable patch 3
- set gdmflexiserver as a default login manager

* Sun Apr 18 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 5.11-1mdv2010.1
+ Revision: 536072
- update to new version 5.11

* Sun Jan 10 2010 Oden Eriksson <oeriksson@mandriva.com> 5.10-2mdv2010.1
+ Revision: 488979
- fix br deps (gdm)
- fix br deps (makedepend)
- rebuilt against libjpeg v8

  + GÃ¶tz Waschk <waschk@mandriva.org>
    - drop patch 21 and call make depend instead

* Thu Sep 10 2009 Frederik Himpe <fhimpe@mandriva.org> 5.10-1mdv2010.0
+ Revision: 437464
- Update to new version 5.10
- Rediff deps patch

* Sun Sep 06 2009 GÃ¶tz Waschk <waschk@mandriva.org> 5.09-1mdv2010.0
+ Revision: 432083
- new version
- rediff patch 11
- drop patch 20
- patch 21: fix deps of some hacks

* Sat Aug 15 2009 Oden Eriksson <oeriksson@mandriva.com> 5.08-4mdv2010.0
+ Revision: 416670
- rebuilt against libjpeg v7

* Mon Jul 20 2009 Colin Guthrie <cguthrie@mandriva.org> 5.08-3mdv2010.0
+ Revision: 398036
- Build with new x11-proto/libxext

* Mon Dec 29 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 5.08-2mdv2009.1
+ Revision: 320794
- Patch9: use xvt script instread of hardcoding default terminal emulator to gnome-terminal

* Sun Dec 28 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 5.08-1mdv2009.1
+ Revision: 320545
- Patch9: rediff to meet nofuzz
- Patch11: rediff to meet nofuzz
- fix buildrequires
- update to new version 5.08

* Sun Sep 07 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 5.07-3mdv2009.0
+ Revision: 282277
- relax perms for real for xscreensaver binary(disabled drop_setgid patch)

* Mon Aug 25 2008 Vincent Danen <vdanen@mandriva.com> 5.07-2mdv2009.0
+ Revision: 275958
- disable the drop_setgid patch for now and relax perms

* Mon Aug 11 2008 GÃ¶tz Waschk <waschk@mandriva.org> 5.07-1mdv2009.0
+ Revision: 270724
- new version
- rediff patches 9,11

* Thu Jul 17 2008 Funda Wang <fwang@mandriva.org> 5.06-1mdv2009.0
+ Revision: 236674
- BR libxinerama-devel
- New version 5.06

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Fri May 23 2008 Vincent Danen <vdanen@mandriva.com> 5.05-4mdv2009.0
+ Revision: 210395
- build without shadow support
- add patch to not call setgid()
- make xscreensaver sgid chkpwd; should work with both tcb and shadow passwords now

* Wed Apr 30 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 5.05-3mdv2009.0
+ Revision: 199448
- move locales to the main package
- do not require xscreensaver-base, since now there is only one screensaver GDadou
- fix file list
- Patch9: tune up timeouts

* Wed Apr 30 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 5.05-2mdv2009.0
+ Revision: 199358
- Patch9: install gdadou.xml config file !
- drop patch 15, use xdg-open
- drop patch 18, use realname for icons
- drop X-MandrivLinux category
- revoke dead configure options and add new ones
- add missing buildrequires on gdm
- kill switches for mdv 2006
- do not require words package (dunno what for this was pulled in)
- spec file clean
- TODO maybe split out mandriva specific plugin gdadou to a separate package
- Patch9: fix chbg syntax
- set the DPMS values

* Mon Mar 03 2008 GÃ¶tz Waschk <waschk@mandriva.org> 5.05-1mdv2008.1
+ Revision: 178160
- new version
- update patch 18
- drop patch 20

* Thu Feb 28 2008 Frederic Crozat <fcrozat@mandriva.com> 5.04-3mdv2008.1
+ Revision: 176409
- Replace mandrake_desk dependency with mandriva-theme-screensaver

* Thu Feb 07 2008 Funda Wang <fwang@mandriva.org> 5.04-2mdv2008.1
+ Revision: 163625
- add ubuntu patch to have it build

  + Thierry Vignaud <tv@mandriva.org>
    - drop old menu
    - fix mesaglu-devel BR
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Wed Nov 14 2007 GÃ¶tz Waschk <waschk@mandriva.org> 5.04-1mdv2008.1
+ Revision: 108691
- new version

* Thu Sep 20 2007 Frederic Crozat <fcrozat@mandriva.com> 5.03-2mdv2008.0
+ Revision: 91461
- Update patch9 with one background color for GDadou
  Update patch18 to remove icon extension

* Tue Jul 17 2007 GÃ¶tz Waschk <waschk@mandriva.org> 5.03-1mdv2008.0
+ Revision: 52868
- fix buildrequires

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - new version

* Sun Apr 22 2007 GÃ¶tz Waschk <waschk@mandriva.org> 5.02-2mdv2008.0
+ Revision: 17004
- fix description

* Sun Apr 22 2007 GÃ¶tz Waschk <waschk@mandriva.org> 5.02-1mdv2008.0
+ Revision: 16951
- new version


* Wed Sep 20 2006 Götz Waschk <waschk@mandriva.org> 5.01-1mdv2007.0
- rediff patch 15
- New version 5.01

* Fri Jul 07 2006 Götz Waschk <waschk@mandriva.org> 5.00-5mdv2007.0
- fix buildrequires

* Thu Jul 06 2006 Frederic Crozat <fcrozat@mandriva.com> 5.00-4mdv2007.0
- Add obsoletes to ease upgrade
- switch to XDG menu

* Wed Jul 05 2006 Thierry Vignaud <tvignaud@mandriva.com> 5.00-3mdv2007.0
- fix upgrade

* Sat Jun 24 2006 Frederic Crozat <fcrozat@mandriva.com> 5.00-2mdv2007.0
- Slip main packages in seperate subpackages (can be used by gnome-screensaver)
- disable kerberos support, use pam instead

* Thu May 25 2006 Götz Waschk <waschk@mandriva.org> 5.00-1mdk
- install in /usr
- drop patch 20
- update patch 9,19
- New release 5.00

* Thu May 18 2006 Laurent MONTEL <lmontel@mandriva.com> 4.24-2
- Rebuild

* Thu Feb 09 2006 Götz Waschk <waschk@mandriva.org> 4.24-1mdk
- rediff patch 19 aka the Jesus patch
- rediff patch 9
- New release 4.24

* Tue Jan 31 2006 Olivier Blin <oblin@mandriva.com> 4.23-3mdk
- use "include" directive instead of deprecated pam_stack (Patch20)

* Tue Nov 22 2005 Götz Waschk <waschk@mandriva.org> 4.23-2mdk
- fix plf build

* Mon Nov 21 2005 Frederic Crozat <fcrozat@mandriva.com> 4.23-1mdk
- Release 4.23
- Patch19:; disable inappropriate stuff in glsnake (Mdk bug #19866)
- Regenerate patch10

* Thu Sep 22 2005 Frederic Crozat <fcrozat@mandriva.com> 4.22-6mdk
- Update patch15 to fix Mdk bug #9320

* Tue Sep 06 2005 Frederic Crozat <fcrozat@mandriva.com> 4.22-5mdk
- Update patch9 to sort images

* Sat Sep 03 2005 Frederic Crozat <fcrozat@mandriva.com> 4.22-4mdk
- Update patch9 with background color based on product

* Tue Jun 28 2005 Andreas Hasenack <andreas@mandriva.com> 4.22-3mdk
- rebuilt without krb4

* Mon Jun 27 2005 Götz Waschk <waschk@mandriva.org> 4.22-2mdk
- drop sources 2,3

* Fri Jun 24 2005 Götz Waschk <waschk@mandriva.org> 4.22-1mdk
- use generated file lists for the hacks
- New release 4.22

* Sat May 14 2005 Götz Waschk <waschk@mandriva.org> 4.21-2mdk
- disable source 2

* Tue Apr 19 2005 Götz Waschk <waschk@linux-mandrake.com> 4.21-1mdk
- fix the --with options
- mkrel
- new hack: fliptext
- update file list
- rediff patch 9
- New release 4.21

* Wed Mar 16 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 4.20-3mdk
- fix icon name (Mdk bug #14650)

* Wed Mar 02 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 4.20-2mdk
- Fix menu name to remove conflict when we call "kcmshell screensaver"

* Thu Feb 24 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 4.20-1mdk
- Release 4.20
- new hacks : boing, boxfix, carousel, fiberlamp
- Regenerate patch15
- Remove patches 19 (no longer relevant), 20 (merged upstream)

* Thu Jan 06 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 4.19-2mdk
- Add patch20: fix launch xscreensaver into kde

* Thu Dec 16 2004 Götz Waschk <waschk@linux-mandrake.com> 4.19-1mdk
- new hacks: substrate, intermomentary, fireworkx and pinion
- new version

* Tue Aug 17 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 4.18-2mdk
- Add patch19: fix kscreebsacer path use '/usr/X11R6/bin' and not '/usr/bin'

* Mon Aug 16 2004 Götz Waschk <waschk@linux-mandrake.com> 4.18-3mdk
- new hacks: anemotaxism, memscroller
- remove double menu entry
- New release 4.17

* Wed Aug 04 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 4.16-3mdk
- Update patch 15 to use xvt instead of xterm (Mdk bug #9320)

* Sat Jul 31 2004 Götz Waschk <waschk@linux-mandrake.com> 4.16-2mdk
- add xscreensaver-demo menu entry

* Fri May 14 2004 Götz Waschk <waschk@linux-mandrake.com> 4.16-1mdk
- add new hacks: antinspect, fuzzyflakes, polyhedra, providence
- drop patch 19
- New release 4.16

* Sat Apr 03 2004 Götz Waschk <waschk@linux-mandrake.com> 4.15-1mdk
- fix description
- add new hacks: mismunch, noof, pacman, wormhole
- fix typo in the kerberos driver
- new version

* Mon Dec 15 2003 Götz Waschk <waschk@linux-mandrake.com> 4.14-4mdk
- fix deps of the subpackages

* Thu Nov 06 2003 Götz Waschk <waschk@linux-mandrake.com> 4.14-3mdk
- enable extrusion and move it to the extrusion subpackage
- rename --with xmatrix to --with plf
- move xmatrix and glmatrix to the matrix subpackage

* Wed Nov 05 2003 Götz Waschk <waschk@linux-mandrake.com> 4.14-2mdk
- remove xmatrix, glmatrix and extrusion (thanks to Christian Bricart)

* Tue Nov 04 2003 Götz Waschk <waschk@linux-mandrake.com> 4.14-1mdk
- add new hacks: apple2, blinkbox, fontglide, gleidescope, mirrorblob, pong,
- add new hack: xanalogtv
- add new program ljlatest
- fix gle buildrequires
- new version
- new version

* Tue Oct 21 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.12-2mdk
- rebuild for rewriting /etc/pam.d file

