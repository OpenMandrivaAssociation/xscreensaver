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

Summary:	A set of X Window System screensavers
Name:		xscreensaver
Version:	5.09
Release:	%mkrel 1
License:	BSD
Group:		Graphical desktop/Other
URL:		http://www.jwz.org/xscreensaver/
Source0:	http://www.jwz.org/xscreensaver/%{name}-%{version}.tar.gz
Source1:	xscreensaver-capplet.png
Patch0:		xscreensaver-5.05-mdv-alt-drop_setgid.patch
# Only GDadou should be enabled
Patch9:		xscreensaver-5.08-defaultconfig.patch
# (fc) 4.00-4mdk allow root to start xscreensaver
Patch10:	xscreensaver-4.23-root.patch
# (fc) 4.05-3mdk disable openGL hacks by default
Patch11:	xscreensaver-5.09-noGL.patch
# (fc) 4.05-4mdk don't show screensavers that aren't available
Patch13:	xscreensaver-4.01-avail.patch
# (fc) 4.23-1mdk disable inappropriate stuff (Mdk bug #19866)
Patch19:	xscreensaver-5.00-inappropriate.patch
Patch21:	xscreensaver-5.09-deps.patch
Requires:	xscreensaver-common = %{version}-%{release}
Requires:	fortune-mod
Requires:	mandriva-theme-screensaver
Requires:	xdg-utils
BuildRequires:	gdm
BuildRequires:	bc
BuildRequires:	fortune-mod
BuildRequires:	libjpeg-devel
BuildRequires:	pam-devel
BuildRequires:	xpm-devel
BuildRequires:	libglade2.0-devel
BuildRequires:	imagemagick
BuildRequires:	mesaglut-devel
BuildRequires:	X11-devel
BuildRequires:	libxext-devel
BuildRequires:	libxxf86misc-devel
BuildRequires:	libxinerama-devel
%if %enable_extrusion
BuildRequires:	libgle-devel
%endif
BuildRequires:	desktop-file-utils
Conflicts:	gnome-control-center < 1.5.11-4mdk
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The xscreensaver package contains a variety of screensavers for your
mind-numbing, ambition-eroding, time-wasting, hypnotized viewing
pleasure.

Install the xscreensaver package if you need screensavers for use with
the X Window System.

%if %plf
This package is in PLF as it contains copyrighted images.
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
Obsoletes:	xscreensaver-utils
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

%if %plf
%package matrix
Summary:	The Matrix screensavers
Group:		Graphical desktop/Other
Requires:	xscreensaver-common = %{version}-%{release}

%description matrix
The xscreensaver-matrix package contains two screensavers for
xscreensaver based on the movie The Matrix. It is in plf because there
might by copyright problems with the artwork used in this
screensavers.
%endif

%if %enable_extrusion
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
#%patch0 -p1 -b .drop_setgid
# WARNING this patch must ALWAYS be applied, if it fails, REGENERATE it !!!
%patch9 -p1 -b .defaultconfig
%patch10 -p1 -b .root
%patch11 -p1 -b .noGL
%patch13 -p1 -b .available
%if %{disable_inappropriate}
%patch19 -p1 -b .inappropriate
%endif
%patch21 -p1

#needed by patches 11, 16
autoconf

%build
%configure2_5x \
    --enable-locking \
    --enable-root-passwd \
    --with-browser=xdg-open \
    --without-sgi-ext \
    --without-xidle-ext \
    --without-sgivc-ext \
    --with-dpms-ext \
    --with-xinerama-ext \
    --with-xf86vmode-ext \
    --with-xf86gamma-ext \
    --with-randr-ext \
    --with-proc-interrupts \
    --with-login-manager \
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
%if %enable_extrusion
    --with-gle 
%else
    --without-gle
%endif

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

cat<<EOF >README.GL
The xscreensaver-gl package contains even more screensavers for your
mind-numbing, ambition-eroding, time-wasting, hypnotized viewing
pleasure. These screensavers require OpenGL or Mesa support.

Install the xscreensaver-gl package if you need more screensavers for
use with the X Window System and you have OpenGL or Mesa installed.
EOF

desktop-file-install \
  --remove-category="Application" \
  --remove-category="AdvancedSettings" \
  --remove-category="Appearance" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

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

%if ! %plf
rm -rf %{buildroot}%{_libexecdir}/xscreensaver/*matrix
rm -rf %{buildroot}%{_mandir}/man6/*matrix*
rm -rf %{buildroot}%{_datadir}/xscreensaver/config/*matrix*
%endif
%if ! %enable_extrusion
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
perl -pi -e "s/.*(xjack|matrix|extrusion).*//" gl-extras.files base.files

%find_lang %{name}

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post 
%{update_menus}
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%clean_icon_cache hicolor
%endif

%post gl
sed -i -e 's/\A-\s+GL:/ GL:/' %{_sysconfdir}/X11/app-defaults/XScreenSaver

%postun gl
sed -i -e '/\A\s*GL:/ and print "- $_" or print "$_"' %{_sysconfdir}/X11/app-defaults/XScreenSaver

%files -f %{name}.lang
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/pam.d/xscreensaver
%doc README
%{_mandir}/man1/xscreensaver-command.1*
%{_mandir}/man1/xscreensaver-demo.1*
%{_mandir}/man1/xscreensaver.1*
%attr(755,root,chkpwd) %{_bindir}/xscreensaver
%{_bindir}/xscreensaver-command
%{_bindir}/xscreensaver-demo
%dir %{_datadir}/xscreensaver
%{_datadir}/xscreensaver/glade
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%{_datadir}/xscreensaver/config/gdadou.xml
%{_iconsdir}/hicolor/*/apps/*.png

%files common 
%defattr(-,root,root)
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
%defattr(-,root,root)
%exclude %{_datadir}/xscreensaver/config/gdadou.xml

%files gl -f gl-extras.files
%defattr(-,root,root)
%doc README.GL

%if %enable_extrusion
%files extrusion
%defattr(-,root,root)
%doc README.GL
%{_datadir}/xscreensaver/config/extrusion.xml
%{_mandir}/man6/extrusion.6*  
%{_libexecdir}/xscreensaver/extrusion
%endif

%if %plf
%files matrix
%defattr(-,root,root)
%doc README.GL
%{_mandir}/man6/xmatrix.6*
%{_mandir}/man6/glmatrix.6*
%{_datadir}/xscreensaver/config/glmatrix.xml
%{_datadir}/xscreensaver/config/xmatrix.xml
%{_libexecdir}/xscreensaver/xmatrix
%{_libexecdir}/xscreensaver/glmatrix
%endif
