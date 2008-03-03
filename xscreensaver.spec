%define release %mkrel 1
%define plf 0
%define enable_extrusion 1
%define disable_inappropriate 1
# Allow --with[out] <feature> at rpm command line build
%{?_with_plf: %{expand: %%global plf 1}}
%{?_without_plf: %{expand: %%global plf 0}}
%{?_with_extrusion: %{expand: %%global enable_extrusion 1}}
%{?_without_extrusion: %{expand: %%global enable_extrusion 0}}
%{?_with_inappropriate: %{expand: %%global disable_inappropriate 0}}
%{?_without_inappropriate: %{expand: %%global disable_inappropriate 1}}

%if %plf
%define distsuffix plf
%define disable_inappropriate 0
%endif
#fixed2
%{?!mkrel:%define mkrel(c:) %{-c: 0.%{-c*}.}%{!?_with_unstable:%(perl -e '$_="%{1}";m/(.\*\\D\+)?(\\d+)$/;$rel=${2}-1;re;print "$1$rel";').%{?subrel:%subrel}%{!?subrel:1}.%{?distversion:%distversion}%{?!distversion:%(echo $[%{mdkversion}/10])}}%{?_with_unstable:%{1}}%{?distsuffix:%distsuffix}%{?!distsuffix:mdk}}

Name:		xscreensaver
Summary:	A set of X Window System screensavers
Version:	5.05
Release:	%release
License:	BSD
Group:		Graphical desktop/Other
URL:		http://www.jwz.org/xscreensaver/

Source0:	http://www.jwz.org/xscreensaver/xscreensaver-%{version}.tar.gz
Source1:	xscreensaver-capplet.png

# Only GDadou should be enabled
Patch9:		xscreensaver-5.00-defaultconfig.patch
# (fc) 4.00-4mdk allow root to start xscreensaver
Patch10:    xscreensaver-4.23-root.patch
# (fc) 4.05-3mdk disable openGL hacks by default
Patch11:	xscreensaver-4.05-noGL.patch
# (fc) 4.05-4mdk don't show screensavers that aren't available
Patch13:    xscreensaver-4.01-avail.patch
# (fc) 4.05-4mdk use $BROWSER to launch a browser
Patch15:    xscreensaver-5.01-browser.patch
# (fc) 4.05-6mdk fix .desktop entry icon and location
Patch18:    xscreensaver-5.05-desktopfile.patch
# (fc) 4.23-1mdk disable inappropriate stuff (Mdk bug #19866)
Patch19:    xscreensaver-5.00-inappropriate.patch
Requires:   xscreensaver-base = %{version}
Requires:	fortune-mod words chbg
Requires:   mandriva-theme-screensaver
BuildRequires:	autoconf2.5
BuildRequires:	bc
BuildRequires:	fortune-mod
BuildRequires:	libjpeg-devel
BuildRequires:	pam-devel
BuildRequires:	xpm-devel
BuildRequires:	libglade2.0-devel
BuildRequires:	ImageMagick

%if %mdkversion <= 200600
BuildRequires:  XFree86
BuildRequires:  libMesaGLU-devel
%else
BuildRequires: mesaglut-devel
BuildRequires: libx11
BuildRequires: libxxf86misc-devel 
%endif
%if %enable_extrusion
BuildRequires:  libgle-devel
%endif
BuildRequires: desktop-file-utils

Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root
Conflicts:	gnome-control-center < 1.5.11-4mdk

%package common
Group:		Graphical desktop/Other
Summary:	Utilities used by xscreensaver screensavers
Conflicts:  xscreensaver < 5.00-2
Obsoletes:  xscreensaver-utils
Provides:  xscreensaver-utils

%description common
Utilities used by xscreensaver screensavers

%package gl
Group:		Graphical desktop/Other
Requires:	xscreensaver-common = %version
Requires(post):	xscreensaver-common = %version
Requires(postun):	xscreensaver-common = %version
Summary:	A set of GL screensavers

%description gl
The xscreensaver-gl package contains even more screensavers for your
mind-numbing, ambition-eroding, time-wasting, hypnotized viewing
pleasure. These screensavers require OpenGL or Mesa support.

Install the xscreensaver-gl package if you need more screensavers for
use with the X Window System and you have OpenGL or Mesa installed.

%description
The xscreensaver package contains a variety of screensavers for your
mind-numbing, ambition-eroding, time-wasting, hypnotized viewing
pleasure.

Install the xscreensaver package if you need screensavers for use with
the X Window System.

%if %plf
This package is in PLF as it contains copyrighted images.
%endif

%package matrix
Group:		Graphical desktop/Other
Requires:	xscreensaver-common = %version
Summary:	The Matrix screensavers

%description matrix
The xscreensaver-matrix package contains two screensavers for
xscreensaver based on the movie The Matrix. It is in plf because there
might by copyright problems with the artwork used in this
screensavers.

%package extrusion
Group:		Graphical desktop/Other
Requires:	xscreensaver-common = %version
Summary:	OpenGL screensaver 

%description extrusion
The xscreensaver-extrusion package contains the extrusion
screensaversfor your mind-numbing, ambition-eroding, time-wasting,
hypnotized viewing pleasure. This screensaver requires OpenGL or Mesa
support.

This screensaver is in a separate package, because it is the only
application for the Mandriva Linux distribution which requires the GLE
extrusion library.

%package base
Group:		Graphical desktop/Other
Summary:	A set of screensavers
Requires:	xscreensaver-common = %version
Conflicts:  xscreensaver < 5.00-2

%description base
Various screensavers used by Xscreensaver.

%prep
%setup -q
# WARNING this patch must ALWAYS be applied, if it fails, REGENERATE it !!!
%patch9 -p1 -b .defaultconfig
%patch10 -p1 -b .root
%patch11 -p1 -b .noGL
%patch13 -p1 -b .available
%patch15 -p1 -b .browser
%patch18 -p1 -b .desktopfile
%if %{disable_inappropriate}
%patch19 -p1 -b .inappropriate
%endif

#needed by patches 11, 16
autoconf

%build

%configure2_5x --prefix=%{_prefix} --exec-prefix=%{_prefix} \
 --libexec=%{_libexecdir} --with-gtk2 --without-gnome \
 --with-zippy="/usr/games/fortune" \
 --without-motif  --with-pam --with-gl \
 --with-image-directory="%_datadir/mdk/screensaver" \
 --without-kerberos \
%if %enable_extrusion
 --with-gle 
%else
 --without-gle
%endif

%make

%install
rm -rf $RPM_BUILD_ROOT gl-extras.files base.files %name.lang
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/app-defaults/
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man6
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pam.d
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/xscreensaver

make install_prefix=$RPM_BUILD_ROOT bindir=%{_bindir} \
 KDEDIR=%{_prefix} GNOME_BINDIR=%{_bindir}  GNOME_DATADIR=%{_datadir} \
 mandir=%{_mandir} AD_DIR=%{_sysconfdir}/X11/app-defaults/ \
 gnulocaledir=%_datadir/locale install

cat<<EOF >README.GL
The xscreensaver-gl package contains even more screensavers for your
mind-numbing, ambition-eroding, time-wasting, hypnotized viewing
pleasure. These screensavers require OpenGL or Mesa support.

Install the xscreensaver-gl package if you need more screensavers for
use with the X Window System and you have OpenGL or Mesa installed.
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
cp %{SOURCE1}  $RPM_BUILD_ROOT%{_datadir}/pixmaps


desktop-file-install --vendor="" \
  --remove-category="Application" \
  --remove-category="AdvancedSettings" \
  --remove-category="Appearance" \
  --add-category="X-MandrivaLinux-System-Configuration-Other" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*
#icons
mkdir -p %buildroot{%_liconsdir,%_iconsdir,%_miconsdir}
convert -scale 32x32 %SOURCE1 %buildroot%_iconsdir/xscreensaver.png
convert -scale 16x16 %SOURCE1 %buildroot%_miconsdir/xscreensaver.png
ln -s %{_datadir}/pixmaps/xscreensaver-capplet.png %buildroot%_liconsdir/xscreensaver.png


#remove unpackaged files
rm -f $RPM_BUILD_ROOT%{_datadir}/xscreensaver/config/xjack.xml
rm -f $RPM_BUILD_ROOT%_mandir/man6/xjack.6  
rm -f  $RPM_BUILD_ROOT%{_libexecdir}/xscreensaver/xjack

%if ! %{plf}
rm -rf $RPM_BUILD_ROOT%{_libexecdir}/xscreensaver/*matrix
rm -rf $RPM_BUILD_ROOT%_mandir/man6/*matrix*
rm -rf $RPM_BUILD_ROOT%{_datadir}/xscreensaver/config/*matrix*
%endif
%if ! %{enable_extrusion}
rm -f $RPM_BUILD_ROOT%{_datadir}/xscreensaver/config/extrusion.xml
rm -f $RPM_BUILD_ROOT%_mandir/man6/extrusion.6
%endif

%find_lang %{name}

# This function prints a list of things that get installed.
# It does this by parsing the output of a dummy run of "make install".
#
list_files() {
  make -s install_prefix=${RPM_BUILD_ROOT} mandir=%{_mandir}/ \
  bindir=%{_bindir} INSTALL=true "$@"	\
   | sed -n -e 's@.* \(/[^ ]*\)$@\1@p'				\
   | sed    -e "s@^${RPM_BUILD_ROOT}@@"				\
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
perl -pi -e "s/.*(xjack|matrix|extrusion).*//" gl-extras.files base.files

%find_lang %{name}
cat %{name}.lang >> $dd/base.files

%clean
rm -rf $RPM_BUILD_ROOT

%post 
%{update_menus}

%postun
%{clean_menus}
%post gl
sed -i -e 's/\A-\s+GL:/ GL:/' %{_sysconfdir}/X11/app-defaults/XScreenSaver

%postun gl
sed -i -e '/\A\s*GL:/ and print "- $_" or print "$_"' %{_sysconfdir}/X11/app-defaults/XScreenSaver

%files 
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/pam.d/xscreensaver
%doc README
%_mandir/man1/xscreensaver-command.1*
%_mandir/man1/xscreensaver-demo.1*
%_mandir/man1/xscreensaver.1*
%{_bindir}/xscreensaver
%{_bindir}/xscreensaver-command
%{_bindir}/xscreensaver-demo
%dir %{_datadir}/xscreensaver
%{_datadir}/xscreensaver/glade
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%_liconsdir/*.png
%_iconsdir/*.png
%_miconsdir/*.png

%files common 
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/X11/app-defaults/*
%dir %{_libexecdir}/xscreensaver/
%{_bindir}/xscreensaver-getimage
%{_bindir}/xscreensaver-getimage-file
%{_bindir}/xscreensaver-getimage-video
%{_bindir}/xscreensaver-text
%_mandir/man1/xscreensaver-getimage*
%_mandir/man1/xscreensaver-text.1*
%dir %_datadir/%name/config
%_datadir/%name/config/README

%files base -f base.files
%defattr(-,root,root)

%files gl -f gl-extras.files
%defattr(-,root,root)
%doc README.GL

%if %enable_extrusion
%files extrusion
%defattr(-,root,root)
%doc README.GL
%{_datadir}/xscreensaver/config/extrusion.xml
%_mandir/man6/extrusion.6*  
%{_libexecdir}/xscreensaver/extrusion
%endif

%if %{plf}
%files matrix
%defattr(-,root,root)
%doc README.GL
%_mandir/man6/xmatrix.6*
%_mandir/man6/glmatrix.6*
%{_datadir}/xscreensaver/config/glmatrix.xml
%{_datadir}/xscreensaver/config/xmatrix.xml
%{_libexecdir}/xscreensaver/xmatrix
%{_libexecdir}/xscreensaver/glmatrix
%endif
