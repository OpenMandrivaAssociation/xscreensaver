%if "%{disttag}" == "mdk"
%define disable_inappropriate 0
%else
%define disable_inappropriate 1
%endif

Summary:	A set of X Window System screensavers
Name:		xscreensaver
Version:	5.32
Release:	1
License:	BSD
Group:		Graphical desktop/Other
URL:		http://www.jwz.org/xscreensaver/
Source0:	http://www.jwz.org/xscreensaver/%{name}-%{version}.tar.gz
Source1:	xscreensaver-capplet.png
Source2:	dmctl
Source3:	update-xscreensaver-hacks
Patch0:		xscreensaver-5.05-mdv-alt-drop_setgid.patch
# Don't check login manager in PATH because we use custom wrapper
Patch1:		xscreensaver-5.15-lmcheck.patch
# Only OpenMandriva should be enabled
Patch9:		xscreensaver-5.32-defaultconfig.patch
# (fc) 4.00-4mdk allow root to start xscreensaver
Patch10:	xscreensaver-4.23-root.patch
# (fc) 4.05-3mdk disable openGL hacks by default
Patch11:	xscreensaver-5.09-noGL.patch

# fedora patches
# bug 129335
# sanitize the names of modes in barcode
Patch1001:          xscreensaver-5.26-sanitize-hacks.patch
## Patches already sent to the upsteam
## Patches which must be discussed with upstream
#
# Change webcollage not to access to net
# Also see bug 472061
Patch1021:         xscreensaver-5.26-webcollage-default-nonet.patch
#
# Update Japanese po file
Patch1032:         xscreensaver-5.13-dpmsQuickoff-japo.patch
# driver/test-passwd tty segfaults
Patch1051:         xscreensaver-5.12-test-passwd-segv-tty.patch
# patch to compile driver/test-xdpms
Patch1052:         xscreensaver-5.12-tests-miscfix.patch

Requires:	xscreensaver-common = %{version}-%{release}
#Requires:	fortune-mod
Requires:	distro-theme-screensaver
Requires:	xdg-utils
Requires:	pam >= 1.1.8-19
BuildRequires:	intltool
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
BuildRequires:	gle-devel
BuildRequires:	imagemagick

%description
The xscreensaver package contains a variety of screensavers for your
mind-numbing, ambition-eroding, time-wasting, hypnotized viewing
pleasure.

Install the xscreensaver package if you need screensavers for use with
the X Window System.

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
Conflicts:	xscreensaver < 5.26-2
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
%rename		%{name}-extrusion
%rename		%{name}-matrix

%description gl
The xscreensaver-gl package contains even more screensavers for your
mind-numbing, ambition-eroding, time-wasting, hypnotized viewing
pleasure. These screensavers require OpenGL or Mesa support.

Install the xscreensaver-gl package if you need more screensavers for
use with the X Window System and you have OpenGL or Mesa installed.

%prep
%setup -q
%patch1 -p1 -b .login-manager
# WARNING this patch must ALWAYS be applied, if it fails, REGENERATE it !!!
%patch9 -p1 -b .defaultconfig
ln -srf po/Makefile.in{,.in}
%patch10 -p1 -b .root
%patch11 -p1 -b .noGL
%if %{disable_inappropriate}
%patch1001 -p1 -b .inappropriate
%endif

%patch1021 -p1
%patch1032 -p1
%patch1051 -p1
%patch1052 -p1

# Needed by patches 1 and 11
autoreconf -fiv

%build
%configure \
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
    --enable-pam-check-account-type \
    --with-gl \
    --with-image-directory=%{_datadir}/mdk/screensaver \
    --with-x-app-defaults=%{_datadir}/X11/app-defaults \
    --without-kerberos \
    --with-text-file=%{_sysconfdir}/release \
    --with-gle
make distdepend
make depend DEPEND="makedepend -I$(%{_cc} -print-search-dirs|sed -e 's#^install: \(.*\).*#\1#g'|head -n1)/include"
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
 mandir=%{_mandir} AD_DIR=%{_datadir}/X11/app-defaults/ \
 gnulocaledir=%{_datadir}/locale install
%makeinstall -C po

install -p -m755 %{SOURCE3} -D %{buildroot}%{_sbindir}/update-xscreensaver-hacks

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
pushd hacks/glx ; list_files install > $dd/gl-extras.files ; popd
pushd hacks     ; list_files install > $dd/base.files; popd

%find_lang %{name}

%post gl
sed -i -e 's/\A-\s+GL:/ GL:/' %{_datadir}/X11/app-defaults/XScreenSaver

%postun gl
sed -i -e '/\A\s*GL:/ and print "- $_" or print "$_"' %{_datadir}/X11/app-defaults/XScreenSaver

%files -f %{name}.lang
%doc README
%config(noreplace) %{_sysconfdir}/pam.d/xscreensaver
%{_mandir}/man1/xscreensaver-command.1*
%{_mandir}/man1/xscreensaver-demo.1*
%{_mandir}/man1/xscreensaver.1*
%attr(755,root,shadow) %{_bindir}/xscreensaver
%{_bindir}/xscreensaver-command
%{_bindir}/xscreensaver-demo
%{_bindir}/dmctl
%{_datadir}/applications/xscreensaver-properties.desktop
%{_datadir}/pixmaps/*
%{_iconsdir}/hicolor/*/apps/*.png

%files common
%{_datadir}/X11/app-defaults/*
%dir %{_libexecdir}/%{name}
%{_bindir}/xscreensaver-getimage
%{_bindir}/xscreensaver-getimage-file
%{_bindir}/xscreensaver-getimage-video
%{_bindir}/xscreensaver-text
%{_mandir}/man1/xscreensaver-getimage*
%{_mandir}/man1/xscreensaver-text.1*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/glade
%{_datadir}/%{name}/glade/*
%dir %{_datadir}/%{name}/config
%{_datadir}/%{name}/config/README

%files base -f base.files
%{_sbindir}/update-xscreensaver-hacks

%files gl -f gl-extras.files
%doc README.GL
